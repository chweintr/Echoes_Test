#!/usr/bin/env python3
"""
Test Vonnegut voice with corrected ID
"""

import asyncio
import aiohttp
import os
from dotenv import load_dotenv

load_dotenv()

async def test_vonnegut():
    """Test the KVJ voice (likely Vonnegut)"""
    
    api_key = os.getenv("ELEVENLABS_API_KEY")
    voice_id = "J80PasKsbR4AWMLiAQ0j"  # KVJ voice (corrected)
    
    vonnegut_text = "So it goes. Hello there, friend. I'm Kurt Vonnegut, speaking to you from the great beyond, which turns out to be remarkably similar to Indianapolis."
    
    print(f"Testing voice ID: {voice_id}")
    print(f"Text: {vonnegut_text}")
    
    async with aiohttp.ClientSession() as session:
        headers = {
            "xi-api-key": api_key,
            "Content-Type": "application/json"
        }
        
        payload = {
            "text": vonnegut_text,
            "model_id": "eleven_monolingual_v1",
            "voice_settings": {
                "stability": 0.7,
                "similarity_boost": 0.85,
                "style": 0.3
            }
        }
        
        async with session.post(
            f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
            headers=headers,
            json=payload
        ) as response:
            
            if response.status == 200:
                audio_data = await response.read()
                
                with open("vonnegut_test.mp3", "wb") as f:
                    f.write(audio_data)
                
                print(f"SUCCESS: Generated Vonnegut voice ({len(audio_data)} bytes)")
                print("Saved as: vonnegut_test.mp3")
                
                # Try to play
                try:
                    import subprocess
                    subprocess.run(["start", "vonnegut_test.mp3"], shell=True)
                    print("Audio should be playing...")
                except:
                    print("Play manually: vonnegut_test.mp3")
                
                return True
            else:
                error = await response.text()
                print(f"FAILED: {error}")
                return False

if __name__ == "__main__":
    asyncio.run(test_vonnegut())