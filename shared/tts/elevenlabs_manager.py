"""
ElevenLabs TTS Manager for Indiana Oracle
Handles voice synthesis with streaming support
"""

import os
import asyncio
import aiohttp
import json
import logging
from typing import AsyncGenerator, Dict, Optional
from dataclasses import dataclass
import base64

logger = logging.getLogger(__name__)

@dataclass
class ElevenLabsConfig:
    """ElevenLabs configuration"""
    api_key: str
    model_id: str = "eleven_monolingual_v1"
    voice_settings: Dict = None
    
    def __post_init__(self):
        if self.voice_settings is None:
            self.voice_settings = {
                "stability": 0.5,
                "similarity_boost": 0.75,
                "style": 0.0,
                "use_speaker_boost": True
            }

class ElevenLabsManager:
    """Manages ElevenLabs TTS for multiple personas"""
    
    def __init__(self, config: Optional[ElevenLabsConfig] = None):
        self.config = config or self._load_config()
        self.session = None
        self.voice_cache = {}
        
        # Voice IDs mapping
        self.voice_ids = {
            "indiana-oracle": "KoVIHoyLDrQyd4pGalbs",  # General Indiana Oracle voice
            "kurt-vonnegut": "J80PasKsbR4AWMLiAQ0jn",  # Vonnegut voice
            "vonnegut": "J80PasKsbR4AWMLiAQ0jn",  # Alias for Vonnegut
            "larry-bird": "21m00Tcm4TlvDq8ikWAM",  # Default voice (Rachel) for now
            "david-letterman": "21m00Tcm4TlvDq8ikWAM",  # Default voice (Rachel) for now
            # Add more as created
        }
        
    def _load_config(self) -> ElevenLabsConfig:
        """Load configuration from environment"""
        api_key = os.getenv("ELEVENLABS_API_KEY", "")
        if not api_key:
            logger.warning("ElevenLabs API key not found in environment")
        
        return ElevenLabsConfig(api_key=api_key)
    
    async def initialize(self):
        """Initialize HTTP session"""
        self.session = aiohttp.ClientSession()
        
        # Verify API key
        if self.config.api_key:
            await self._verify_api_key()
    
    async def _verify_api_key(self):
        """Verify the API key is valid"""
        try:
            headers = {"xi-api-key": self.config.api_key}
            
            async with self.session.get(
                "https://api.elevenlabs.io/v1/user",
                headers=headers
            ) as response:
                if response.status == 200:
                    user_info = await response.json()
                    logger.info(f"ElevenLabs connected: {user_info.get('xi_api_key')[:8]}...")
                else:
                    logger.error("Invalid ElevenLabs API key")
        except Exception as e:
            logger.error(f"Error verifying ElevenLabs API key: {e}")
    
    async def get_voices(self) -> Dict:
        """Get list of available voices"""
        try:
            headers = {"xi-api-key": self.config.api_key}
            
            async with self.session.get(
                "https://api.elevenlabs.io/v1/voices",
                headers=headers
            ) as response:
                if response.status == 200:
                    return await response.json()
        except Exception as e:
            logger.error(f"Error getting voices: {e}")
        
        return {"voices": []}
    
    async def create_voice(self, name: str, files: list, description: str = "") -> Optional[str]:
        """Create a custom voice from audio files"""
        try:
            headers = {"xi-api-key": self.config.api_key}
            
            data = aiohttp.FormData()
            data.add_field("name", name)
            data.add_field("description", description)
            
            # Add audio files
            for file_path in files:
                with open(file_path, 'rb') as f:
                    data.add_field(
                        "files",
                        f,
                        filename=os.path.basename(file_path),
                        content_type="audio/mpeg"
                    )
            
            async with self.session.post(
                "https://api.elevenlabs.io/v1/voices/add",
                headers=headers,
                data=data
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    voice_id = result.get("voice_id")
                    logger.info(f"Created voice '{name}' with ID: {voice_id}")
                    return voice_id
                else:
                    error = await response.text()
                    logger.error(f"Failed to create voice: {error}")
                    
        except Exception as e:
            logger.error(f"Error creating voice: {e}")
        
        return None
    
    async def synthesize(self, text: str, persona_id: str) -> Optional[bytes]:
        """Synthesize speech (non-streaming)"""
        voice_id = self.voice_ids.get(persona_id, "21m00Tcm4TlvDq8ikWAM")
        
        try:
            headers = {
                "xi-api-key": self.config.api_key,
                "Content-Type": "application/json"
            }
            
            payload = {
                "text": text,
                "model_id": self.config.model_id,
                "voice_settings": self.config.voice_settings
            }
            
            async with self.session.post(
                f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
                headers=headers,
                json=payload
            ) as response:
                if response.status == 200:
                    return await response.read()
                else:
                    error = await response.text()
                    logger.error(f"TTS synthesis failed: {error}")
                    
        except Exception as e:
            logger.error(f"Error in TTS synthesis: {e}")
        
        return None
    
    async def stream_tts(
        self, 
        text: str, 
        persona_id: str
    ) -> AsyncGenerator[Dict, None]:
        """Stream TTS audio with word timing data"""
        
        voice_id = self.voice_ids.get(persona_id, "21m00Tcm4TlvDq8ikWAM")
        
        try:
            headers = {
                "xi-api-key": self.config.api_key,
                "Content-Type": "application/json"
            }
            
            payload = {
                "text": text,
                "model_id": "eleven_monolingual_v1",
                "voice_settings": self.config.voice_settings,
                "generation_config": {
                    "chunk_length_schedule": [50],  # 50ms chunks
                }
            }
            
            # Use streaming endpoint
            async with self.session.post(
                f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}/stream-input",
                headers=headers,
                json=payload
            ) as response:
                
                if response.status != 200:
                    error = await response.text()
                    logger.error(f"Streaming TTS failed: {error}")
                    return
                
                # Read streaming response
                async for chunk in response.content.iter_chunked(1024):
                    if chunk:
                        # Convert to base64 for transport
                        audio_base64 = base64.b64encode(chunk).decode('utf-8')
                        
                        yield {
                            "type": "audio_chunk",
                            "audio_base64": audio_base64,
                            "audio_bytes": chunk,
                            "timestamp": asyncio.get_event_loop().time()
                        }
                        
        except Exception as e:
            logger.error(f"Error in TTS streaming: {e}")
    
    async def stream_tts_websocket(
        self,
        text: str,
        persona_id: str,
        websocket_callback
    ):
        """Stream TTS via WebSocket for lowest latency"""
        
        voice_id = self.voice_ids.get(persona_id, "21m00Tcm4TlvDq8ikWAM")
        
        try:
            # ElevenLabs WebSocket endpoint
            ws_url = f"wss://api.elevenlabs.io/v1/text-to-speech/{voice_id}/stream-input?model_id=eleven_monolingual_v1"
            
            headers = {
                "xi-api-key": self.config.api_key,
            }
            
            async with self.session.ws_connect(ws_url, headers=headers) as ws:
                # Send configuration
                await ws.send_json({
                    "text": " ",  # Start with space
                    "voice_settings": self.config.voice_settings,
                    "generation_config": {
                        "chunk_length_schedule": [50],
                    },
                    "xi_api_key": self.config.api_key,
                })
                
                # Send text in chunks for faster response
                words = text.split()
                chunk_size = 5  # Words per chunk
                
                for i in range(0, len(words), chunk_size):
                    chunk = " ".join(words[i:i+chunk_size])
                    await ws.send_json({
                        "text": chunk + " ",
                        "try_trigger_generation": True,
                    })
                
                # Send end of input
                await ws.send_json({
                    "text": "",
                })
                
                # Receive audio chunks
                async for msg in ws:
                    if msg.type == aiohttp.WSMsgType.TEXT:
                        data = json.loads(msg.data)
                        
                        if data.get("audio"):
                            # Decode base64 audio
                            audio_bytes = base64.b64decode(data["audio"])
                            
                            await websocket_callback({
                                "type": "audio_chunk",
                                "audio_bytes": audio_bytes,
                                "audio_base64": data["audio"],
                                "is_final": data.get("isFinal", False)
                            })
                            
                    elif msg.type == aiohttp.WSMsgType.ERROR:
                        logger.error(f"WebSocket error: {ws.exception()}")
                        break
                        
        except Exception as e:
            logger.error(f"Error in WebSocket TTS: {e}")
    
    def get_voice_id(self, persona_id: str) -> str:
        """Get ElevenLabs voice ID for a persona"""
        return self.voice_ids.get(persona_id, "21m00Tcm4TlvDq8ikWAM")
    
    async def update_voice_settings(self, persona_id: str, settings: Dict):
        """Update voice settings for a persona"""
        # Store custom settings per persona
        if not hasattr(self, 'persona_settings'):
            self.persona_settings = {}
        
        self.persona_settings[persona_id] = settings
        logger.info(f"Updated voice settings for {persona_id}: {settings}")
    
    async def close(self):
        """Close HTTP session"""
        if self.session:
            await self.session.close()


# Utility function for quick testing
async def test_elevenlabs():
    """Test ElevenLabs integration"""
    manager = ElevenLabsManager()
    await manager.initialize()
    
    # Test Indiana Oracle voice
    test_text = "Welcome to the Indiana Oracle. I am here to share the stories of our state."
    
    # Non-streaming test
    audio = await manager.synthesize(test_text, "indiana-oracle")
    if audio:
        with open("test_oracle_voice.mp3", "wb") as f:
            f.write(audio)
        logger.info("Saved test audio to test_oracle_voice.mp3")
    
    await manager.close()


if __name__ == "__main__":
    # Run test
    asyncio.run(test_elevenlabs())