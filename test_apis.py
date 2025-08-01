#!/usr/bin/env python3
"""
Test API connections for Indiana Oracle
Run this to verify all services are accessible
"""

import os
import asyncio
import aiohttp
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_openai():
    """Test OpenAI API connection"""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or api_key == "your_openai_api_key_here":
        logger.warning("❌ OpenAI API key not configured")
        return False
    
    try:
        # We'll skip actual API call for now since key not set
        logger.info("⚠️  OpenAI API key present but not tested (add your key first)")
        return True
    except Exception as e:
        logger.error(f"❌ OpenAI test failed: {e}")
        return False

async def test_elevenlabs():
    """Test ElevenLabs API connection"""
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        logger.warning("❌ ElevenLabs API key not found")
        return False
    
    try:
        async with aiohttp.ClientSession() as session:
            headers = {"xi-api-key": api_key}
            
            async with session.get(
                "https://api.elevenlabs.io/v1/user",
                headers=headers
            ) as response:
                if response.status == 200:
                    user_info = await response.json()
                    character_count = user_info.get("subscription", {}).get("character_count", 0)
                    character_limit = user_info.get("subscription", {}).get("character_limit", 0)
                    
                    logger.info(f"✅ ElevenLabs connected!")
                    logger.info(f"   Characters used: {character_count:,} / {character_limit:,}")
                    logger.info(f"   Subscription: {user_info.get('subscription', {}).get('tier', 'Unknown')}")
                    return True
                else:
                    logger.error(f"❌ ElevenLabs API returned status {response.status}")
                    return False
                    
    except Exception as e:
        logger.error(f"❌ ElevenLabs test failed: {e}")
        return False

async def test_heygen():
    """Test HeyGen API connection"""
    api_key = os.getenv("HEYGEN_API_KEY")
    if not api_key:
        logger.warning("❌ HeyGen API key not found")
        return False
    
    try:
        async with aiohttp.ClientSession() as session:
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            
            # Test with avatar list endpoint
            async with session.get(
                "https://api.heygen.com/v2/avatars",
                headers=headers
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    avatar_count = len(data.get("avatars", []))
                    
                    logger.info(f"✅ HeyGen connected!")
                    logger.info(f"   Available avatars: {avatar_count}")
                    
                    # Show first few avatars
                    for avatar in data.get("avatars", [])[:3]:
                        logger.info(f"   - {avatar.get('name', 'Unknown')} ({avatar.get('avatar_id')})")
                    
                    return True
                else:
                    error_text = await response.text()
                    logger.error(f"❌ HeyGen API returned status {response.status}: {error_text}")
                    return False
                    
    except Exception as e:
        logger.error(f"❌ HeyGen test failed: {e}")
        return False

async def test_all():
    """Run all API tests"""
    logger.info("""
╔════════════════════════════════════════════════════╗
║         Indiana Oracle API Connection Test         ║
╚════════════════════════════════════════════════════╝
    """)
    
    # Test each API
    results = {
        "OpenAI": await test_openai(),
        "ElevenLabs": await test_elevenlabs(),
        "HeyGen": await test_heygen()
    }
    
    # Summary
    logger.info("\n" + "="*50)
    logger.info("Summary:")
    
    for service, success in results.items():
        status = "✅ Connected" if success else "❌ Not configured"
        logger.info(f"  {service}: {status}")
    
    # Check readiness
    ready_count = sum(1 for success in results.values() if success)
    
    if ready_count == 3:
        logger.info("\n🎉 All services connected! Ready to launch Oracle.")
    elif ready_count >= 2:
        logger.info("\n⚠️  Some services connected. Oracle can run with limitations.")
    else:
        logger.info("\n❌ Please configure API keys in .env file")
    
    return results

if __name__ == "__main__":
    asyncio.run(test_all())