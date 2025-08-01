#!/usr/bin/env python3
"""
Main Oracle System - Manages all personas and real-time interactions
"""

import asyncio
import json
import logging
from typing import Dict, Optional
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Import persona modules
from personas.persona_manager import PersonaManager
from shared.audio.speech_recognition import SpeechRecognizer
from shared.tts.tts_manager import TTSManager
from shared.avatar.avatar_manager import AvatarManager
from backend.websocket.streaming_handler import StreamingHandler

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OracleSystem:
    def __init__(self):
        self.app = FastAPI(title="Indiana Oracle Entity Project")
        self.setup_cors()
        
        # Initialize managers
        self.persona_manager = PersonaManager()
        self.speech_recognizer = SpeechRecognizer()
        self.tts_manager = TTSManager()
        self.avatar_manager = AvatarManager()
        self.streaming_handler = StreamingHandler()
        
        # Active sessions
        self.active_sessions: Dict[str, Dict] = {}
        
        # Setup routes
        self.setup_routes()
        
        logger.info("Oracle System initialized")
    
    def setup_cors(self):
        """Configure CORS for web access"""
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    
    def setup_routes(self):
        """Setup FastAPI routes"""
        
        @self.app.get("/")
        async def root():
            return {
                "name": "Indiana Oracle Entity Project",
                "status": "active",
                "personas": self.persona_manager.list_personas()
            }
        
        @self.app.get("/personas")
        async def list_personas():
            """List all available personas"""
            return self.persona_manager.get_persona_info()
        
        @self.app.websocket("/oracle/session")
        async def oracle_session(websocket: WebSocket):
            """Main WebSocket endpoint for real-time interaction"""
            await self.handle_oracle_session(websocket)
        
        @self.app.post("/persona/{persona_id}/preview")
        async def preview_persona(persona_id: str, text: str):
            """Generate preview audio for a persona"""
            return await self.generate_preview(persona_id, text)
    
    async def handle_oracle_session(self, websocket: WebSocket):
        """Handle real-time oracle session"""
        await websocket.accept()
        session_id = f"session_{id(websocket)}"
        
        try:
            # Initialize session
            self.active_sessions[session_id] = {
                "websocket": websocket,
                "current_persona": "main-oracle",
                "conversation_history": [],
                "stream_active": False
            }
            
            # Send welcome message
            await websocket.send_json({
                "type": "welcome",
                "message": "Welcome to the Indiana Oracle. Who would you like to speak with?",
                "personas": self.persona_manager.list_personas()
            })
            
            # Handle messages
            while True:
                data = await websocket.receive_json()
                await self.process_message(session_id, data)
                
        except WebSocketDisconnect:
            logger.info(f"Session {session_id} disconnected")
        except Exception as e:
            logger.error(f"Session error: {e}")
        finally:
            if session_id in self.active_sessions:
                del self.active_sessions[session_id]
    
    async def process_message(self, session_id: str, data: Dict):
        """Process incoming WebSocket message"""
        message_type = data.get("type")
        session = self.active_sessions[session_id]
        websocket = session["websocket"]
        
        if message_type == "select_persona":
            # Switch to selected persona
            persona_id = data.get("persona_id")
            success = await self.switch_persona(session_id, persona_id)
            
            if success:
                persona = self.persona_manager.get_persona(persona_id)
                await websocket.send_json({
                    "type": "persona_selected",
                    "persona": persona_id,
                    "greeting": persona.get_greeting(),
                    "avatar_ready": await self.avatar_manager.prepare_avatar(persona_id)
                })
        
        elif message_type == "audio_stream_start":
            # Start receiving audio stream
            session["stream_active"] = True
            await self.streaming_handler.start_stream(session_id)
        
        elif message_type == "audio_chunk":
            # Process audio chunk
            if session["stream_active"]:
                audio_data = data.get("audio")
                await self.process_audio_chunk(session_id, audio_data)
        
        elif message_type == "audio_stream_end":
            # End audio stream and process
            session["stream_active"] = False
            await self.finalize_audio_processing(session_id)
        
        elif message_type == "text_input":
            # Direct text input (fallback)
            text = data.get("text")
            await self.process_text_input(session_id, text)
    
    async def switch_persona(self, session_id: str, persona_id: str) -> bool:
        """Switch to a different persona"""
        try:
            session = self.active_sessions[session_id]
            
            # Validate persona exists
            if not self.persona_manager.persona_exists(persona_id):
                return False
            
            # Trigger transition effect
            await session["websocket"].send_json({
                "type": "transition_start",
                "effect": "particle_dissolve"
            })
            
            # Switch persona
            session["current_persona"] = persona_id
            session["conversation_history"] = []
            
            # Load persona-specific models
            await self.avatar_manager.load_persona(persona_id)
            await self.tts_manager.load_voice(persona_id)
            
            return True
            
        except Exception as e:
            logger.error(f"Error switching persona: {e}")
            return False
    
    async def process_audio_chunk(self, session_id: str, audio_data: str):
        """Process incoming audio chunk"""
        session = self.active_sessions[session_id]
        
        # Add to audio buffer
        await self.streaming_handler.add_audio_chunk(session_id, audio_data)
        
        # Perform real-time transcription
        partial_text = await self.speech_recognizer.transcribe_partial(audio_data)
        
        if partial_text:
            await session["websocket"].send_json({
                "type": "transcription_partial",
                "text": partial_text
            })
    
    async def finalize_audio_processing(self, session_id: str):
        """Finalize audio processing and generate response"""
        session = self.active_sessions[session_id]
        websocket = session["websocket"]
        
        try:
            # Get final transcription
            audio_buffer = await self.streaming_handler.get_audio_buffer(session_id)
            final_text = await self.speech_recognizer.transcribe_final(audio_buffer)
            
            await websocket.send_json({
                "type": "transcription_final",
                "text": final_text
            })
            
            # Get persona response
            persona = self.persona_manager.get_persona(session["current_persona"])
            response = await persona.get_response(
                final_text, 
                session["conversation_history"]
            )
            
            # Update conversation history
            session["conversation_history"].extend([
                {"role": "user", "content": final_text},
                {"role": "assistant", "content": response}
            ])
            
            # Generate TTS with avatar data
            await self.stream_response(session_id, response)
            
        except Exception as e:
            logger.error(f"Error processing audio: {e}")
            await websocket.send_json({
                "type": "error",
                "message": "Error processing your request"
            })
    
    async def stream_response(self, session_id: str, response_text: str):
        """Stream TTS audio with avatar data"""
        session = self.active_sessions[session_id]
        websocket = session["websocket"]
        persona_id = session["current_persona"]
        
        # Start response
        await websocket.send_json({
            "type": "response_start",
            "text": response_text
        })
        
        # Stream TTS with avatar sync
        async for chunk in self.tts_manager.stream_tts(response_text, persona_id):
            # Get avatar blend shapes for this audio chunk
            blend_shapes = await self.avatar_manager.get_blend_shapes(
                chunk["audio"], 
                persona_id
            )
            
            # Send synchronized data
            await websocket.send_json({
                "type": "response_chunk",
                "audio": chunk["audio_base64"],
                "blend_shapes": blend_shapes,
                "visemes": chunk.get("visemes", {}),
                "emotion": chunk.get("emotion", "neutral")
            })
        
        # End response
        await websocket.send_json({
            "type": "response_end"
        })
    
    async def process_text_input(self, session_id: str, text: str):
        """Process text input (fallback for audio)"""
        session = self.active_sessions[session_id]
        
        # Get persona response
        persona = self.persona_manager.get_persona(session["current_persona"])
        response = await persona.get_response(
            text,
            session["conversation_history"]
        )
        
        # Update history
        session["conversation_history"].extend([
            {"role": "user", "content": text},
            {"role": "assistant", "content": response}
        ])
        
        # Stream response
        await self.stream_response(session_id, response)
    
    def run(self, host: str = "0.0.0.0", port: int = 8000):
        """Run the Oracle server"""
        logger.info(f"Starting Indiana Oracle on {host}:{port}")
        uvicorn.run(self.app, host=host, port=port)


def main():
    """Main entry point"""
    oracle = OracleSystem()
    oracle.run()


if __name__ == "__main__":
    main()