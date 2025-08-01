#!/usr/bin/env python3
"""
List all available voices in your ElevenLabs account
"""

import asyncio
import aiohttp
import os
from dotenv import load_dotenv

load_dotenv()

async def list_voices():
    """List all voices in the account"""
    
    api_key = os.getenv("ELEVENLABS_API_KEY")
    
    async with aiohttp.ClientSession() as session:
        headers = {"xi-api-key": api_key}
        
        async with session.get(
            "https://api.elevenlabs.io/v1/voices",
            headers=headers
        ) as response:
            
            if response.status == 200:
                data = await response.json()
                voices = data.get("voices", [])
                
                print(f"FOUND {len(voices)} VOICES:")
                print("=" * 50)
                
                for voice in voices:
                    name = voice.get("name", "Unknown")
                    voice_id = voice.get("voice_id", "Unknown")
                    category = voice.get("category", "Unknown")
                    
                    print(f"Name: {name}")
                    print(f"ID: {voice_id}")
                    print(f"Category: {category}")
                    print("-" * 30)
                
                return voices
            else:
                print(f"Failed to get voices: {response.status}")
                return []

if __name__ == "__main__":
    asyncio.run(list_voices())