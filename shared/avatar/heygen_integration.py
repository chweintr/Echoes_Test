"""
HeyGen Streaming Avatar Integration
Real-time avatar streaming for Indiana Oracle
"""

import asyncio
import aiohttp
import json
import logging
from typing import Dict, Optional, AsyncGenerator
import os
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class HeyGenConfig:
    """HeyGen configuration"""
    api_key: str
    avatar_ids: Dict[str, str]  # persona_id -> heygen_avatar_id mapping
    voice_ids: Dict[str, str]   # persona_id -> heygen_voice_id mapping
    streaming_endpoint: str = "https://api.heygen.com/v1/streaming.new"
    
class HeyGenAvatarManager:
    """Manages HeyGen streaming avatars for multiple personas"""
    
    def __init__(self, config: Optional[HeyGenConfig] = None):
        self.config = config or self._load_config()
        self.active_sessions: Dict[str, Dict] = {}
        self.session = None
        
    def _load_config(self) -> HeyGenConfig:
        """Load HeyGen configuration from environment"""
        return HeyGenConfig(
            api_key=os.getenv("HEYGEN_API_KEY", ""),
            avatar_ids={
                "vonnegut": "your_vonnegut_avatar_id",
                "larry-bird": "your_larry_bird_avatar_id",
                "david-letterman": "your_letterman_avatar_id",
                # Add more as you create them
            },
            voice_ids={
                "vonnegut": "your_vonnegut_voice_id",
                "larry-bird": "your_larry_bird_voice_id", 
                "david-letterman": "your_letterman_voice_id",
            }
        )
    
    async def initialize(self):
        """Initialize HTTP session"""
        self.session = aiohttp.ClientSession()
    
    async def create_streaming_session(self, persona_id: str) -> Dict:
        """Create a new HeyGen streaming session for a persona"""
        
        if not self.config.api_key:
            logger.error("HeyGen API key not configured")
            return {"error": "HeyGen not configured"}
        
        avatar_id = self.config.avatar_ids.get(persona_id)
        voice_id = self.config.voice_ids.get(persona_id)
        
        if not avatar_id:
            logger.error(f"No HeyGen avatar configured for {persona_id}")
            return {"error": f"No avatar for {persona_id}"}
        
        try:
            headers = {
                "Authorization": f"Bearer {self.config.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "avatar_id": avatar_id,
                "voice": {
                    "voice_id": voice_id or "default"
                },
                "streaming_features": {
                    "real_time": True,
                    "low_latency": True
                }
            }
            
            async with self.session.post(
                self.config.streaming_endpoint,
                headers=headers,
                json=payload
            ) as response:
                
                if response.status == 200:
                    session_data = await response.json()
                    session_id = session_data.get("session_id")
                    
                    self.active_sessions[session_id] = {
                        "persona_id": persona_id,
                        "ws_url": session_data.get("ws_url"),
                        "ice_servers": session_data.get("ice_servers"),
                        "session_token": session_data.get("session_token")
                    }
                    
                    logger.info(f"Created HeyGen session for {persona_id}: {session_id}")
                    return session_data
                else:
                    error_msg = await response.text()
                    logger.error(f"HeyGen session creation failed: {error_msg}")
                    return {"error": error_msg}
                    
        except Exception as e:
            logger.error(f"Error creating HeyGen session: {e}")
            return {"error": str(e)}
    
    async def stream_text_to_avatar(
        self, 
        session_id: str, 
        text: str
    ) -> AsyncGenerator[Dict, None]:
        """Stream text to HeyGen avatar and get video/audio responses"""
        
        session = self.active_sessions.get(session_id)
        if not session:
            logger.error(f"No active session: {session_id}")
            return
        
        ws_url = session["ws_url"]
        
        try:
            async with self.session.ws_connect(ws_url) as ws:
                # Send authentication
                await ws.send_json({
                    "type": "auth",
                    "token": session["session_token"]
                })
                
                # Send text for avatar to speak
                await ws.send_json({
                    "type": "speak",
                    "text": text,
                    "settings": {
                        "speed": 1.0,
                        "emotion": "neutral"
                    }
                })
                
                # Receive streaming responses
                async for msg in ws:
                    if msg.type == aiohttp.WSMsgType.TEXT:
                        data = json.loads(msg.data)
                        
                        if data["type"] == "stream_chunk":
                            yield {
                                "type": "avatar_chunk",
                                "video_data": data.get("video_base64"),
                                "audio_data": data.get("audio_base64"),
                                "lip_sync": data.get("lip_sync"),
                                "timestamp": data.get("timestamp")
                            }
                        elif data["type"] == "stream_end":
                            break
                            
                    elif msg.type == aiohttp.WSMsgType.ERROR:
                        logger.error(f'WebSocket error: {ws.exception()}')
                        break
                        
        except Exception as e:
            logger.error(f"Error in avatar streaming: {e}")
    
    async def get_avatar_preview(self, persona_id: str) -> Optional[bytes]:
        """Get a preview image of the avatar"""
        avatar_id = self.config.avatar_ids.get(persona_id)
        if not avatar_id:
            return None
        
        try:
            headers = {"Authorization": f"Bearer {self.config.api_key}"}
            
            async with self.session.get(
                f"https://api.heygen.com/v1/avatars/{avatar_id}/preview",
                headers=headers
            ) as response:
                if response.status == 200:
                    return await response.read()
                    
        except Exception as e:
            logger.error(f"Error getting avatar preview: {e}")
            
        return None
    
    async def close_session(self, session_id: str):
        """Close a HeyGen streaming session"""
        if session_id in self.active_sessions:
            # Call HeyGen API to close session
            try:
                headers = {"Authorization": f"Bearer {self.config.api_key}"}
                
                await self.session.delete(
                    f"{self.config.streaming_endpoint}/{session_id}",
                    headers=headers
                )
                
            except Exception as e:
                logger.error(f"Error closing session: {e}")
            
            del self.active_sessions[session_id]
    
    async def close(self):
        """Close all sessions and cleanup"""
        for session_id in list(self.active_sessions.keys()):
            await self.close_session(session_id)
        
        if self.session:
            await self.session.close()


# Alternative: Audio2Face Integration (if HeyGen not available)
class Audio2FaceManager:
    """NVIDIA Audio2Face integration for avatar animation"""
    
    def __init__(self, a2f_url: str = "http://localhost:8011"):
        self.a2f_url = a2f_url
        self.session = None
        
    async def initialize(self):
        """Initialize connection to Audio2Face"""
        self.session = aiohttp.ClientSession()
        
        # Test connection
        try:
            async with self.session.get(f"{self.a2f_url}/status") as response:
                if response.status == 200:
                    logger.info("Connected to Audio2Face")
                else:
                    logger.warning("Audio2Face not responding")
        except:
            logger.error("Could not connect to Audio2Face")
    
    async def get_blend_shapes(self, audio_chunk: bytes) -> Dict[str, float]:
        """Get facial blend shapes from audio chunk"""
        try:
            async with self.session.post(
                f"{self.a2f_url}/audio_to_face",
                data=audio_chunk,
                headers={"Content-Type": "audio/wav"}
            ) as response:
                if response.status == 200:
                    return await response.json()
                    
        except Exception as e:
            logger.error(f"Audio2Face error: {e}")
            
        return {}
    
    async def close(self):
        """Close session"""
        if self.session:
            await self.session.close()