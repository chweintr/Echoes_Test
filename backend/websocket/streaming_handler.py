"""
Real-time streaming handler for audio/video WebSocket communication
"""

import asyncio
import base64
import json
import logging
from typing import Dict, Optional
from collections import defaultdict
import numpy as np

logger = logging.getLogger(__name__)

class StreamingHandler:
    """Handles real-time audio/video streaming via WebSocket"""
    
    def __init__(self):
        self.audio_buffers: Dict[str, list] = defaultdict(list)
        self.stream_metadata: Dict[str, Dict] = {}
        self.sample_rate = 16000  # Standard for speech recognition
        
    async def start_stream(self, session_id: str, metadata: Optional[Dict] = None):
        """Initialize a new streaming session"""
        self.audio_buffers[session_id] = []
        self.stream_metadata[session_id] = metadata or {
            "start_time": asyncio.get_event_loop().time(),
            "chunks_received": 0,
            "sample_rate": self.sample_rate
        }
        logger.info(f"Started stream for session {session_id}")
    
    async def add_audio_chunk(self, session_id: str, audio_base64: str):
        """Add audio chunk to buffer"""
        try:
            # Decode base64 audio
            audio_bytes = base64.b64decode(audio_base64)
            
            # Convert to numpy array (assuming 16-bit PCM)
            audio_array = np.frombuffer(audio_bytes, dtype=np.int16)
            
            # Add to buffer
            self.audio_buffers[session_id].extend(audio_array)
            
            # Update metadata
            if session_id in self.stream_metadata:
                self.stream_metadata[session_id]["chunks_received"] += 1
            
            # Check if we should process (every 0.5 seconds of audio)
            chunk_size = int(self.sample_rate * 0.5)
            if len(self.audio_buffers[session_id]) >= chunk_size:
                return True  # Ready to process
                
        except Exception as e:
            logger.error(f"Error adding audio chunk: {e}")
            
        return False
    
    async def get_audio_buffer(self, session_id: str) -> np.ndarray:
        """Get the complete audio buffer for a session"""
        if session_id in self.audio_buffers:
            return np.array(self.audio_buffers[session_id], dtype=np.int16)
        return np.array([], dtype=np.int16)
    
    async def clear_buffer(self, session_id: str):
        """Clear audio buffer for a session"""
        if session_id in self.audio_buffers:
            self.audio_buffers[session_id] = []
    
    async def end_stream(self, session_id: str):
        """End a streaming session"""
        if session_id in self.audio_buffers:
            del self.audio_buffers[session_id]
        if session_id in self.stream_metadata:
            del self.stream_metadata[session_id]
        logger.info(f"Ended stream for session {session_id}")
    
    def get_stream_stats(self, session_id: str) -> Dict:
        """Get statistics for a streaming session"""
        if session_id not in self.stream_metadata:
            return {}
        
        metadata = self.stream_metadata[session_id]
        current_time = asyncio.get_event_loop().time()
        duration = current_time - metadata["start_time"]
        
        return {
            "duration": duration,
            "chunks_received": metadata["chunks_received"],
            "buffer_size": len(self.audio_buffers.get(session_id, [])),
            "estimated_seconds": len(self.audio_buffers.get(session_id, [])) / self.sample_rate
        }