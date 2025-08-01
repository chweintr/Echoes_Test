#!/usr/bin/env python3
"""
Simple voice test for Indiana Oracle
Let's get basic text-to-speech working first
"""

import os
import asyncio
from dotenv import load_dotenv

# Load environment
load_dotenv()

def test_local_tts():
    """Test local Windows TTS as fallback"""
    print("Testing local Windows TTS...")
    
    try:
        import pyttsx3
        
        engine = pyttsx3.init()
        
        # Get available voices
        voices = engine.getProperty('voices')
        print(f"Found {len(voices)} voices:")
        
        for i, voice in enumerate(voices[:3]):  # Show first 3
            print(f"  {i}: {voice.name}")
        
        # Test speech
        test_text = "Hello, I am the Indiana Oracle. Welcome to our state's history."
        print(f"\nSpeaking: '{test_text}'")
        
        engine.say(test_text)
        engine.runAndWait()
        
        print("✓ Local TTS working!")
        return True
        
    except Exception as e:
        print(f"✗ Local TTS failed: {e}")
        return False

async def test_elevenlabs():
    """Test ElevenLabs API"""
    api_key = os.getenv("ELEVENLABS_API_KEY")
    
    if not api_key:
        print("✗ No ElevenLabs API key found")
        return False
    
    print(f"Testing ElevenLabs with key: {api_key[:8]}...")
    
    try:
        import aiohttp
        
        async with aiohttp.ClientSession() as session:
            headers = {"xi-api-key": api_key}
            
            # Test API connection
            async with session.get(
                "https://api.elevenlabs.io/v1/user",
                headers=headers
            ) as response:
                
                if response.status == 200:
                    user_info = await response.json()
                    print("✓ ElevenLabs connected!")
                    print(f"  Subscription: {user_info.get('subscription', {}).get('tier', 'Unknown')}")
                    
                    # Test basic TTS
                    test_text = "Hello from Indiana Oracle"
                    
                    async with session.post(
                        "https://api.elevenlabs.io/v1/text-to-speech/21m00Tcm4TlvDq8ikWAM",  # Rachel voice
                        headers=headers,
                        json={
                            "text": test_text,
                            "model_id": "eleven_monolingual_v1",
                            "voice_settings": {
                                "stability": 0.5,
                                "similarity_boost": 0.75
                            }
                        }
                    ) as tts_response:
                        
                        if tts_response.status == 200:
                            audio_data = await tts_response.read()
                            
                            # Save test file
                            with open("test_voice.mp3", "wb") as f:
                                f.write(audio_data)
                            
                            print(f"✓ Generated voice file: test_voice.mp3 ({len(audio_data)} bytes)")
                            return True
                        else:
                            error = await tts_response.text()
                            print(f"✗ TTS failed: {error}")
                            return False
                else:
                    error = await response.text()
                    print(f"✗ ElevenLabs auth failed: {error}")
                    return False
                    
    except Exception as e:
        print(f"✗ ElevenLabs test failed: {e}")
        return False

def test_browser_interface():
    """Test if we can serve the basic interface"""
    print("Testing browser interface...")
    
    import webbrowser
    import http.server
    import socketserver
    import threading
    import time
    from pathlib import Path
    
    try:
        # Check if interface file exists
        interface_file = Path("frontend/web/oracle_interface.html")
        if not interface_file.exists():
            print(f"✗ Interface file not found: {interface_file}")
            return False
        
        print(f"✓ Interface file found: {interface_file}")
        
        # Start simple server
        PORT = 8080
        
        class Handler(http.server.SimpleHTTPRequestHandler):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, directory="frontend/web", **kwargs)
        
        def run_server():
            with socketserver.TCPServer(("", PORT), Handler) as httpd:
                httpd.serve_forever()
        
        server_thread = threading.Thread(target=run_server, daemon=True)
        server_thread.start()
        
        time.sleep(1)
        
        print(f"✓ Server started on http://localhost:{PORT}")
        print("  You can manually open: http://localhost:8080/oracle_interface.html")
        
        return True
        
    except Exception as e:
        print(f"✗ Server test failed: {e}")
        return False

async def main():
    """Run all basic tests"""
    print("""
====================================================
INDIANA ORACLE - BASIC FUNCTIONALITY TEST
====================================================
    """)
    
    tests = [
        ("Local TTS", test_local_tts),
        ("ElevenLabs API", test_elevenlabs),
        ("Browser Interface", test_browser_interface)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        print(f"\n--- {test_name} ---")
        try:
            if asyncio.iscoroutinefunction(test_func):
                result = await test_func()
            else:
                result = test_func()
            results[test_name] = result
        except Exception as e:
            print(f"✗ {test_name} crashed: {e}")
            results[test_name] = False
    
    # Summary
    print(f"\n{'='*50}")
    print("TEST SUMMARY:")
    print(f"{'='*50}")
    
    for test_name, result in results.items():
        status = "PASS" if result else "FAIL"
        print(f"{test_name:20} : {status}")
    
    passed = sum(results.values())
    total = len(results)
    
    print(f"\nPassed: {passed}/{total}")
    
    if passed > 0:
        print("\n✓ Some functionality working - we can build from here!")
        if results.get("Browser Interface"):
            print("  → Try opening: http://localhost:8080/oracle_interface.html")
        if results.get("Local TTS"):
            print("  → Local voice synthesis working")
    else:
        print("\n✗ Nothing working yet - let's fix the basics first")
    
    return passed > 0

if __name__ == "__main__":
    asyncio.run(main())