#!/usr/bin/env python3
"""
Test full voice pipeline: OpenAI + ElevenLabs
"""

import asyncio
import aiohttp
import base64
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

async def test_oracle_voice():
    """Test complete Indiana Oracle voice pipeline"""
    
    print("TESTING FULL VOICE PIPELINE")
    print("=" * 40)
    
    # Initialize OpenAI
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    # Test message
    test_question = "Tell me about Indiana's most famous author"
    print(f"Question: {test_question}")
    
    # Indiana Oracle system prompt
    system_prompt = """You are the Indiana Oracle, a wise entity that embodies the collective wisdom and memory of Indiana. You speak with warmth and Midwestern humility, sharing stories about Indiana's history, culture, and people. Keep responses to 1-2 sentences for voice conversation."""
    
    try:
        # Step 1: Get AI response
        print("\n1. Getting AI response...")
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": test_question}
            ],
            max_tokens=100,
            temperature=0.7
        )
        
        oracle_text = response.choices[0].message.content
        print(f"Oracle says: {oracle_text}")
        
        # Step 2: Convert to speech with ElevenLabs
        print("\n2. Converting to speech...")
        
        api_key = os.getenv("ELEVENLABS_API_KEY")
        voice_id = "KoVIHoyLDrQyd4pGalbs"  # Indiana Oracle voice
        
        async with aiohttp.ClientSession() as session:
            headers = {
                "xi-api-key": api_key,
                "Content-Type": "application/json"
            }
            
            payload = {
                "text": oracle_text,
                "model_id": "eleven_monolingual_v1",
                "voice_settings": {
                    "stability": 0.6,
                    "similarity_boost": 0.8,
                    "style": 0.2
                }
            }
            
            async with session.post(
                f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
                headers=headers,
                json=payload
            ) as tts_response:
                
                if tts_response.status == 200:
                    audio_data = await tts_response.read()
                    
                    # Save audio file
                    with open("oracle_response.mp3", "wb") as f:
                        f.write(audio_data)
                    
                    print(f"SUCCESS: Generated voice file ({len(audio_data)} bytes)")
                    print("Saved as: oracle_response.mp3")
                    
                    # Try to play it
                    try:
                        import subprocess
                        import platform
                        
                        if platform.system() == "Windows":
                            # Use Windows Media Player
                            subprocess.run(["start", "oracle_response.mp3"], shell=True)
                            print("Audio should be playing now...")
                        
                    except Exception as e:
                        print(f"Could not auto-play: {e}")
                        print("Manually play: oracle_response.mp3")
                    
                    return True
                    
                else:
                    error = await tts_response.text()
                    print(f"TTS FAILED: {error}")
                    return False
                    
    except Exception as e:
        print(f"ERROR: {e}")
        return False

async def test_vonnegut_voice():
    """Test Vonnegut voice"""
    
    print("\n" + "=" * 40)
    print("TESTING VONNEGUT VOICE")
    print("=" * 40)
    
    # Vonnegut-style response
    vonnegut_text = "So it goes. Hello there, friend. I'm Kurt Vonnegut, speaking to you from whatever comes after Indianapolis, which turns out to be more Indianapolis."
    
    print(f"Vonnegut says: {vonnegut_text}")
    
    api_key = os.getenv("ELEVENLABS_API_KEY")
    voice_id = "J80PasKsbR4AWMLiAQ0j"  # Vonnegut voice (KVJ)
    
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
                
                with open("vonnegut_response.mp3", "wb") as f:
                    f.write(audio_data)
                
                print(f"SUCCESS: Generated Vonnegut voice ({len(audio_data)} bytes)")
                print("Saved as: vonnegut_response.mp3")
                
                return True
            else:
                error = await response.text()
                print(f"FAILED: {error}")
                return False

async def main():
    """Test both voices"""
    
    oracle_ok = await test_oracle_voice()
    vonnegut_ok = await test_vonnegut_voice()
    
    print("\n" + "=" * 40)
    print("FINAL RESULTS:")
    print("=" * 40)
    print(f"Indiana Oracle voice: {'SUCCESS' if oracle_ok else 'FAILED'}")
    print(f"Vonnegut voice: {'SUCCESS' if vonnegut_ok else 'FAILED'}")
    
    if oracle_ok and vonnegut_ok:
        print("\n[SUCCESS] BOTH VOICES WORKING!")
        print("Ready to build full Oracle system!")
    elif oracle_ok or vonnegut_ok:
        print("\n[OK] At least one voice working - good progress!")
    else:
        print("\n[ERROR] Neither voice working - check API keys")

if __name__ == "__main__":
    asyncio.run(main())