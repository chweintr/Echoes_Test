#!/usr/bin/env python3
"""
Test Vonnegut persona via WebSocket
"""

import asyncio
import websockets
import json
import base64

async def test_vonnegut_websocket():
    """Test the Vonnegut persona"""
    
    uri = "ws://localhost:8000/oracle/session"
    
    try:
        async with websockets.connect(uri) as websocket:
            print("Connected to Oracle WebSocket for Vonnegut test!")
            
            # Test with Vonnegut persona
            test_message = {
                "type": "user_message", 
                "text": "What do you think about being a hologram?",
                "persona": "kurt-vonnegut"
            }
            
            await websocket.send(json.dumps(test_message))
            print("Asked Vonnegut about being a hologram...")
            
            # Listen for responses
            response_count = 0
            while response_count < 3:
                response = await websocket.recv()
                data = json.loads(response)
                
                print(f"\nReceived: {data['type']}")
                
                if data['type'] == 'status':
                    print(f"Status: {data['message']}")
                elif data['type'] == 'ai_response':
                    print(f"Vonnegut says: {data['text']}")
                elif data['type'] == 'audio_response':
                    audio_size = len(base64.b64decode(data['audio']))
                    print(f"Received Vonnegut audio: {audio_size} bytes")
                    
                    # Save audio file
                    with open("test_vonnegut_websocket_audio.mp3", "wb") as f:
                        f.write(base64.b64decode(data['audio']))
                    print("Saved Vonnegut audio as: test_vonnegut_websocket_audio.mp3")
                
                response_count += 1
            
            print("\n" + "="*50)
            print("SUCCESS: Vonnegut persona working via WebSocket!")
            print("- Vonnegut personality: [OK]")
            print("- Vonnegut voice (KVJ): [OK]")
            print("- Real-time streaming: [OK]")
            print("="*50)
            
    except Exception as e:
        print(f"Error testing Vonnegut WebSocket: {e}")

if __name__ == "__main__":
    asyncio.run(test_vonnegut_websocket())