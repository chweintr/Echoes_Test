#!/usr/bin/env python3
"""
Direct ElevenLabs API test
"""

import asyncio
import aiohttp

async def test_direct():
    """Test ElevenLabs API directly"""
    
    api_key = "sk_439d393c93299620377f7d1faa5029709392c2b32c906865"
    
    print(f"Testing ElevenLabs with key ending: ...{api_key[-6:]}")
    
    async with aiohttp.ClientSession() as session:
        headers = {"xi-api-key": api_key}
        
        print("Testing /v1/user endpoint...")
        async with session.get(
            "https://api.elevenlabs.io/v1/user",
            headers=headers
        ) as response:
            print(f"Status: {response.status}")
            text = await response.text()
            print(f"Response: {text[:200]}...")
            
            if response.status == 200:
                print("SUCCESS: ElevenLabs connected!")
                
                # Test voices
                print("\nTesting /v1/voices endpoint...")
                async with session.get(
                    "https://api.elevenlabs.io/v1/voices",
                    headers=headers
                ) as voices_response:
                    if voices_response.status == 200:
                        voices_data = await voices_response.json()
                        voices = voices_data.get("voices", [])
                        print(f"Found {len(voices)} voices:")
                        
                        for voice in voices[:5]:  # Show first 5
                            print(f"  - {voice.get('name')} ({voice.get('voice_id')})")
                    else:
                        print(f"Voices failed: {voices_response.status}")
            else:
                print(f"FAILED: {response.status}")

if __name__ == "__main__":
    asyncio.run(test_direct())