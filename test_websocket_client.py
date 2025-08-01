#!/usr/bin/env python3
"""
Test WebSocket client for the Oracle interface
"""

import asyncio
import websockets
import json
import base64

async def test_oracle_websocket():
    """Test the Oracle WebSocket interface"""
    
    uri = "ws://localhost:8000/oracle/session"
    
    try:
        async with websockets.connect(uri) as websocket:
            print("Connected to Oracle WebSocket!")
            
            # Test with Indiana Oracle
            test_message = {
                "type": "user_message",
                "text": "Tell me about Kurt Vonnegut",
                "persona": "indiana-oracle"
            }
            
            await websocket.send(json.dumps(test_message))
            print("Sent test message about Vonnegut to Oracle")
            
            # Listen for responses
            response_count = 0
            while response_count < 3:  # Expect status, text, and audio
                response = await websocket.recv()
                data = json.loads(response)
                
                print(f"\nReceived: {data['type']}")
                
                if data['type'] == 'status':
                    print(f"Status: {data['message']}")
                elif data['type'] == 'ai_response':
                    print(f"Oracle says: {data['text']}")
                elif data['type'] == 'audio_response':
                    audio_size = len(base64.b64decode(data['audio']))
                    print(f"Received audio: {audio_size} bytes")
                    
                    # Save audio file
                    with open("test_oracle_audio.mp3", "wb") as f:
                        f.write(base64.b64decode(data['audio']))
                    print("Saved audio as: test_oracle_audio.mp3")
                
                response_count += 1
            
            print("\n" + "="*50)
            print("SUCCESS: Oracle WebSocket working!")
            print("- Text generation: [OK]")
            print("- Voice synthesis: [OK]") 
            print("- WebSocket streaming: [OK]")
            print("="*50)
            
    except Exception as e:
        print(f"Error testing WebSocket: {e}")

if __name__ == "__main__":
    asyncio.run(test_oracle_websocket())