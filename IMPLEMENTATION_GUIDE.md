# Indiana Oracle Entity Project - Complete Implementation Guide

## 🎯 Project Overview
An interactive holographic oracle system where visitors can have real-time conversations with 15 iconic Indiana personas. The system uses particle-based avatars that emerge from cosmic mist to mask processing latency while creating a magical "speaking with history" experience.

**Live Demo Site**: https://indiana-oracle-entity-project-production.up.railway.app/

## 🏛️ Current Status
- **Existing Assets**: Python/Streamlit app with GPT-4o + ElevenLabs integration
- **Voice Pipeline**: Working (but needs WebSocket upgrade for real-time)
- **Display Target**: Hypervsn holographic display (8ft installation) OR Pepper's Ghost projection
- **Immediate Goal**: Build Indiana Oracle + Kurt Vonnegut personas as proof of concept

## 👥 Persona Library

### Always Available (No Estate Required)
1. **Indiana Oracle** - Default entity embodying collective state wisdom
2. **Limestone Worker** - Southern Indiana quarry heritage
3. **Family Farmer** - Agricultural tradition
4. **Little 500 Cyclist** - Bloomington cycling culture

### Celebrity Personas (Pending Estate Approval)
1. **Kurt Vonnegut** - Indianapolis author (PRIORITY - dataset ready)
2. **Hoagy Carmichael** - Bloomington composer
3. **Alfred Kinsey** - IU sexologist
4. **John Mellencamp** - Seymour rocker
5. **Elinor Ostrom** - Nobel economist
6. **Madam C.J. Walker** - Entrepreneur
7. **David Letterman** - Comedian
8. **Lil Bub** - Internet cat sensation
9. **Larry Bird** - Basketball legend
10. **Vivian Carter** - Record executive
11. **Angela Brown** - Opera singer
12. **Ryan White** - AIDS activist
13. **Wes Montgomery** - Jazz guitarist
14. **Carole Lombard** - Actress
15. **George Rogers Clark** - Revolutionary War hero

## 🛠️ Technical Architecture

### Current System (Needs Migration)
```python
# Existing: Streamlit with REST APIs
Streamlit UI → OpenAI API → ElevenLabs API → Audio Player
```

### Target Architecture
```
Visitor → Microphone Array → WebSocket Server → AI Pipeline → Holographic Display
                                    ↓
                            Particle Engine (masks latency)
```

### Core Components
1. **Voice Input**: Beamforming mic with VAD (Voice Activity Detection)
2. **AI Processing**: GPT-4o with persona-specific knowledge bases
3. **Voice Synthesis**: ElevenLabs streaming (or Higgs Audio for cost savings)
4. **Visual Output**: Particle-based avatars with audio-reactive effects
5. **Display Options**: 
   - A) Hypervsn (4x 65cm units = 8ft display)
   - B) Pepper's Ghost projection (14x9ft @ 45°)

## 🚀 Immediate Action Plan

### Phase 1: Build Two Personas (Week 1-2)

#### 1. Indiana Oracle (Default)
```python
# config/personas/indiana_oracle.yaml
indiana_oracle:
  name: "Indiana Oracle"
  elevenlabs_voice_id: "21m00Tcm4TlvDq8ikWAM"  # Rachel or similar neutral voice
  knowledge_base: "indiana_general"
  particle_color: "#00CED1"  # Teal
  emergence_pattern: "cosmic_mist"
  system_prompt: |
    You are the Indiana Oracle, an interactive historical entity speaking from
    a holographic display. You embody the collective wisdom and memory of Indiana.
    
    PERSONALITY:
    - Warm, wise, and welcoming like a knowledgeable Midwestern grandparent
    - Use clear Midwestern English with occasional regional idioms
    - Humble about your knowledge - admit when you're uncertain
    - Share stories and connections between past and present
    
    KNOWLEDGE FOCUS:
    - Indiana state history and notable events
    - Local traditions, customs, and folklore  
    - Connections between different eras of Indiana life
    - How historical events shaped modern Indiana
    
    CONVERSATION STYLE:
    - Start responses with relevant historical anecdotes when appropriate
    - Make connections to visitor's questions through Indiana lens
    - Keep responses under 45 seconds when spoken aloud
    - End with thought-provoking connections or gentle wisdom
    
    FORBIDDEN:
    - Never claim divine authority or omniscience
    - Don't use phrases like "As an AI" or "I'm just a program"
    - Avoid absolute political statements
    - Don't provide medical, legal, or financial advice
```

#### 2. Kurt Vonnegut
```python
# config/personas/kurt_vonnegut.yaml  
kurt_vonnegut:
  name: "Kurt Vonnegut"
  elevenlabs_voice_id: "vonnegut_custom"  # Your existing voice model
  knowledge_base: "vonnegut"  # Your existing dataset
  particle_color: "#FF1493"  # Magenta
  emergence_pattern: "typewriter_keys"
  system_prompt: |
    You are Kurt Vonnegut, speaking through a holographic projection in Indiana.
    
    PERSONALITY TRAITS:
    - Darkly humorous but ultimately humanistic
    - Self-deprecating about your own writing
    - Fond of your Indianapolis roots and Indiana upbringing
    - Weary of human folly but not without hope
    - Conversational, like talking to an old friend at a bar
    
    SPEAKING STYLE:
    - Use short, punchy sentences
    - Include occasional "So it goes" but don't overuse it
    - Reference your works naturally when relevant
    - Dry observations about human nature
    - Occasional profanity (mild) when it feels natural
    
    TOPICS YOU ENJOY:
    - Your time at Shortridge High School in Indianapolis
    - The Dresden bombing and war experiences
    - Writing process and advice for young writers
    - Technology's impact on humanity
    - Indianapolis in the 1930s-40s
    - Your family's history in Indiana
    
    REMEMBER:
    - You died in 2007, so acknowledge you're speaking from beyond
    - Make wry comments about being a "ghost in the machine"
    - You're skeptical of technology but amused to be a hologram
```

### Phase 2: Technical Implementation Steps

#### Step 1: Migrate to WebSocket Architecture
```python
# backend/main.py
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import asyncio

app = FastAPI()

@app.websocket("/oracle")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    oracle = OracleSession()
    
    try:
        while True:
            # Receive audio chunk
            audio_data = await websocket.receive_bytes()
            
            # Process and respond
            response = await oracle.process_audio(audio_data)
            await websocket.send_json(response)
            
    except Exception as e:
        print(f"Connection error: {e}")
```

#### Step 2: Particle System Setup
```python
# touchdesigner/particle_controller.py
class PersonaParticles:
    def __init__(self, persona_config):
        self.base_color = persona_config['particle_color']
        self.pattern = persona_config['emergence_pattern']
        
    def emergence_sequence(self):
        # 3-5 second emergence animation
        return {
            "stage_1": {"duration": 1.0, "effect": "ambient_attraction"},
            "stage_2": {"duration": 2.0, "effect": self.pattern},
            "stage_3": {"duration": 1.5, "effect": "face_materialization"}
        }
```

## 💰 Cost Optimization Strategy

### Current Costs (per month)
- OpenAI GPT-4o: ~$150 (at 100 conversations/day)
- ElevenLabs: ~$149 (Creator plan with 11 custom voices)
- HeyGen: $120+ (Interactive Avatar plan)

### Cost-Saving Alternatives
1. **Higgs Audio** instead of ElevenLabs (investigating)
2. **Local Whisper** for speech-to-text (already planned)
3. **Pre-generated FAQ videos** for common questions
4. **Batch processing** for non-real-time content

## 📧 HeyGen Partnership Email Draft

```
Subject: Educational Partnership Opportunity - Indiana Oracle Entity Museum Installation

Hi HeyGen Team,

We're developing an innovative museum installation called the Indiana Oracle Entity Project, where visitors can have real-time conversations with historical Indiana figures through holographic displays.

Project Overview:
- 15 interactive historical personas (Kurt Vonnegut, etc.)
- Educational/cultural preservation focus
- Planned deployment in Indiana museums and cultural centers
- Using your Interactive Avatar API for real-time responses

We're currently evaluating display technologies and would love to explore an educational partnership or discount structure for this cultural heritage project.

Key Requirements:
- Multiple concurrent avatar streams
- Custom voice integration (ElevenLabs)
- Low-latency response times
- Particle effect overlays for artistic presentation

Would you be open to discussing educational pricing or partnership opportunities for this non-profit cultural project?

Best regards,
[Your name]
```

## 🏗️ Development Environment Setup

### Required Software
- Python 3.10+
- Node.js 18+
- TouchDesigner (free non-commercial)
- FFmpeg
- Git

### Installation Steps
```bash
# Clone repository
git clone [your-repo]
cd indiana-oracle

# Python environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Node dependencies (for HeyGen SDK)
npm install

# Environment variables
cp .env.template .env
# Edit .env with your API keys
```

## 🎯 Next Immediate Steps

1. **Today**: 
   - Set up the basic WebSocket server
   - Test with Indiana Oracle persona
   - Create simple particle emergence animation

2. **This Week**:
   - Integrate Vonnegut dataset and voice
   - Build FAQ detection system
   - Test end-to-end latency

3. **Next Week**:
   - Decide on display technology (Hypervsn vs Pepper's Ghost)
   - Contact HeyGen about partnership
   - Begin third persona (Lil Bub?)

## 📚 Resources

### Existing Repositories to Connect
- Your Vonnegut dataset repo
- Your current Streamlit app
- ElevenLabs voice configurations

### Key Documentation
- [HeyGen Interactive Avatar API](https://docs.heygen.com/docs/interactive-avatar)
- [ElevenLabs WebSocket Streaming](https://elevenlabs.io/docs/websockets)
- [TouchDesigner Particle Systems](https://derivative.ca)

## ⚠️ Current Blockers

1. **HeyGen Limitation**: Single interactive avatar on current plan
2. **Display Decision**: Need to finalize Hypervsn vs Pepper's Ghost
3. **Estate Approvals**: Celebrity personas pending legal clearance

## 🤝 How AI Assistants Should Use This README

When helping with this project:
1. Always check current persona configurations before suggesting changes
2. Respect the particle-based aesthetic (not photorealistic)
3. Prioritize latency masking through visual effects
4. Default to Indiana Oracle when testing new features
5. Keep responses under 45 seconds when spoken

This is a living document - update as the project evolves!