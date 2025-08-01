#!/usr/bin/env python3
"""
Test basic voice conversation with local TTS
"""

import pyttsx3
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

def test_conversation():
    """Test OpenAI + Local TTS conversation"""
    
    # Initialize OpenAI
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    # Initialize local TTS
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    
    # Use David voice (more masculine for Indiana Oracle)
    engine.setProperty('voice', voices[0].id)  # David
    engine.setProperty('rate', 150)  # Slightly slower
    
    print("VOICE CONVERSATION TEST")
    print("=" * 30)
    print("Type 'quit' to exit")
    print()
    
    # Indiana Oracle system prompt
    system_prompt = """You are the Indiana Oracle, a wise entity that embodies the collective wisdom and memory of Indiana. You speak with warmth and Midwestern humility, sharing stories and connections about Indiana's history, culture, and people. Keep responses under 2 sentences for voice conversation."""
    
    conversation = [{"role": "system", "content": system_prompt}]
    
    while True:
        # Get user input
        user_input = input("You: ").strip()
        
        if user_input.lower() in ['quit', 'exit', 'q']:
            engine.say("Farewell, friend. Until we meet again in the echoes of Indiana.")
            engine.runAndWait()
            break
        
        if not user_input:
            continue
        
        try:
            # Add user message
            conversation.append({"role": "user", "content": user_input})
            
            # Get AI response
            print("Oracle: [thinking...]")
            
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=conversation,
                max_tokens=100,  # Keep it short for voice
                temperature=0.7
            )
            
            oracle_response = response.choices[0].message.content
            
            # Add to conversation history
            conversation.append({"role": "assistant", "content": oracle_response})
            
            # Keep only last 6 messages (3 exchanges)
            if len(conversation) > 7:  # system + 6 messages
                conversation = [conversation[0]] + conversation[-6:]
            
            print(f"Oracle: {oracle_response}")
            
            # Speak the response
            engine.say(oracle_response)
            engine.runAndWait()
            
        except Exception as e:
            print(f"Error: {e}")
            engine.say("I apologize, but I'm having trouble connecting to my thoughts right now.")
            engine.runAndWait()

if __name__ == "__main__":
    test_conversation()