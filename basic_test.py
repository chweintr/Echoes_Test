#!/usr/bin/env python3
"""
Basic functionality test - no fancy Unicode
"""

import os
from dotenv import load_dotenv

load_dotenv()

def test_local_voice():
    """Test if local TTS works"""
    print("Testing local text-to-speech...")
    
    try:
        import pyttsx3
        
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        
        print(f"Found {len(voices)} voices")
        for i, voice in enumerate(voices):
            print(f"  {i}: {voice.name}")
        
        # Quick test
        engine.say("Indiana Oracle voice test")
        engine.runAndWait()
        
        print("SUCCESS: Local voice working!")
        return True
        
    except Exception as e:
        print(f"FAILED: {e}")
        return False

def test_api_keys():
    """Check if API keys are set"""
    print("\nChecking API keys...")
    
    keys = {
        'OPENAI_API_KEY': os.getenv('OPENAI_API_KEY'),
        'ELEVENLABS_API_KEY': os.getenv('ELEVENLABS_API_KEY'), 
        'HEYGEN_API_KEY': os.getenv('HEYGEN_API_KEY')
    }
    
    for name, key in keys.items():
        if key and key != "your_key_here":
            print(f"  {name}: CONFIGURED")
        else:
            print(f"  {name}: MISSING")
    
    return True

def test_web_interface():
    """Check if web files exist"""
    print("\nChecking web interface...")
    
    from pathlib import Path
    
    files = [
        "frontend/web/oracle_interface.html",
        "backend/main_oracle.py",
        "config/personas_detailed.yaml"
    ]
    
    for file_path in files:
        if Path(file_path).exists():
            print(f"  {file_path}: EXISTS")
        else:
            print(f"  {file_path}: MISSING")
    
    return True

def main():
    print("INDIANA ORACLE - BASIC SYSTEM CHECK")
    print("=" * 40)
    
    tests = [
        test_local_voice,
        test_api_keys, 
        test_web_interface
    ]
    
    for test in tests:
        try:
            test()
        except Exception as e:
            print(f"Test crashed: {e}")
    
    print("\n" + "=" * 40)
    print("Next steps:")
    print("1. Fix ElevenLabs API key")
    print("2. Add OpenAI API key") 
    print("3. Test simple voice conversation")

if __name__ == "__main__":
    main()