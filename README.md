# Indiana Oracle Entity Project

A real-time interactive installation where visitors converse with Indiana's historical figures through holographic particle avatars.

## 🎭 Persona Status & Development Plans

### Kurt Vonnegut Persona
**Current Status: ROBUST IMPLEMENTATION**
- ✅ **Comprehensive System Prompt**: Full biographical accuracy, personality modeling, proper "So it goes" usage
- ✅ **Voice Integration**: ElevenLabs voice ID `J80PasKsbR4AWMLiAQ0j` (KVJ voice) with volume boost
- ✅ **Limited Training Data**: 1 transcript from Slaughterhouse-Five readings (23 FAQ entries)
- ✅ **Authentic Personality**: Anti-war perspective, dark humor, Indianapolis roots, self-deprecating style

**Future Development Plans:**
1. **Public Domain Expansion**: Continuously add public domain Vonnegut materials:
   - Letters and interviews in public archives
   - Academic papers and critiques
   - Historical speeches and recordings
   - Library of Congress digitized materials

2. **Estate Collaboration**: 
   - Respectfully approach Vonnegut estate/Kurt Vonnegut Museum & Library
   - Seek permission for educational/cultural use of published works
   - Propose revenue sharing for museum support
   - Ensure authentic representation aligned with Vonnegut's values

3. **Enhanced Training Corpus**:
   - Target books: Slaughterhouse-Five, Cat's Cradle, The Sirens of Titan
   - Include Iowa Writers' Workshop teaching materials
   - Add Indianapolis-specific references and local knowledge
   - Incorporate humanist philosophy and anti-war sentiment

### Indiana Oracle Persona  
**Current Status: ENHANCED WITH RAG SYSTEM**
- ✅ **Robust System Prompt**: Comprehensive Indiana/Bloomington knowledge
- ✅ **Simple RAG Integration**: 8 documents with semantic search
- ✅ **Voice Integration**: ElevenLabs voice ID `KoVIHoyLDrQyd4pGalbs` (Autumn Veil)
- ✅ **Local Expertise**: IU history, Little 500, Showers Factory, limestone industry
- ✅ **Confident Storytelling**: Enhanced prompts encourage specific anecdotes over generalizations

**Current Knowledge Base (RAG System):**
1. Indiana Statehood History (1816)
2. Indiana University Timeline (1820-present)
3. Kurt Vonnegut Biography
4. Indianapolis Motor Speedway History
5. Indiana Limestone Industry
6. Granfalloon Festival & Bloomington Vonnegut Legacy
7. Upland Brewing & Campus Culture
8. Mies van der Rohe Glass House Architecture
9. The Dunnkirk Library Speakeasy & Nightlife Culture

**Future Development Plans:**
1. **Comprehensive Knowledge Base** (120+ sources planned):
   - Indiana Historical Society archives
   - IU Libraries digital collections
   - Bloomington/Monroe County records
   - Indigenous peoples' history (Miami, Potawatomi)
   - Industrial heritage (steel, automotive, pharmaceuticals)
   - Contemporary issues (environment, infrastructure)

2. **Real-time Data Integration**:
   - Weather API for current Bloomington conditions
   - IU Athletics API for sports scores/schedules
   - Local events calendar integration
   - Indiana government data feeds

3. **Advanced RAG Features**:
   - Vector database upgrade (pgvector/FAISS)
   - Quarterly knowledge base updates
   - Source citation and verification
   - Multi-modal content (images, audio, video)

**Knowledge Base Strategy:**
- **Documents vs Stories**: Each "document" contains multiple stories/facts chunked for search
- **Quality over Quantity**: Focus on 50-100 rich, well-researched documents rather than thousands of fragments
- **Latency Optimization**: Current 9-document system has <200ms search times
- **Story Variety**: Each document contains 3-5 distinct anecdotes to reduce repetition
- **Regular Updates**: Monthly addition of 2-3 new documents with seasonal/topical content

**Local Knowledge Research Plan:**
- **Local Expert Network**: Partner with IU graduates, Bloomington historians, longtime residents
- **Research Agent AI**: Deploy specialized AI agents to scour local archives, newspapers, blogs
- **Fact Verification**: Cross-reference all local claims with multiple sources
- **Gap Detection**: Monitor conversations to identify knowledge gaps (like Dunnkirk Library speakeasy)
- **Community Sourcing**: Create submission system for locals to contribute verified stories
- **Monthly Reviews**: Regular audits to catch and correct hallucinated information

## Project Structure

```
indiana-oracle-main/
├── personas/              # Individual persona modules
│   ├── vonnegut/         # Kurt Vonnegut persona
│   ├── main-oracle/      # Main Oracle interface
│   ├── larry-bird/       # Larry Bird persona
│   └── david-letterman/  # David Letterman persona
├── shared/               # Shared components
│   ├── audio/           # Audio processing (VAD, STT)
│   ├── tts/             # Text-to-speech (ElevenLabs, local)
│   ├── avatar/          # Avatar systems (HeyGen, Audio2Face)
│   └── particles/       # TouchDesigner particle systems
├── backend/             # Server infrastructure
│   ├── api/            # FastAPI endpoints
│   ├── websocket/      # Real-time streaming
│   └── streaming/      # Avatar streaming pipeline
├── frontend/           # User interfaces
│   ├── web/           # Web-based interface
│   └── touchdesigner/ # TD particle systems
├── config/            # Configuration files
└── tests/            # Test suites
```

## Technology Stack

### Real-Time Avatar Options

1. **HeyGen Streaming Avatar** (Primary)
   - Business plan for multiple personas
   - Low latency (<500ms)
   - Professional quality

2. **Audio2Face + TouchDesigner** (Backup)
   - NVIDIA Omniverse (free)
   - Custom particle system
   - Full control over aesthetics

### Core Components

- **Speech Recognition**: OpenAI Whisper
- **AI Responses**: GPT-4o 
- **Voice Synthesis**: ElevenLabs (15 custom voices)
- **Avatar Rendering**: HeyGen or Audio2Face
- **Particle Effects**: TouchDesigner
- **Streaming**: WebSocket + WebRTC

## Personas

1. Kurt Vonnegut - Novelist
2. Larry Bird - Basketball Legend
3. David Letterman - TV Host
4. Hoagy Carmichael - Jazz Composer
5. John Mellencamp - Rock Musician
6. Alfred Kinsey - Sexologist
7. Madam C.J. Walker - Entrepreneur
8. Carole Lombard - Actress
9. Wes Montgomery - Jazz Guitarist
10. Elinor Ostrom - Economist
11. Ryan White - Activist
12. Vivian Carter - Music Executive
13. Angela Brown - Opera Singer
14. George Rogers Clark - Revolutionary Hero
15. Lil Bub - Internet Cat

## Installation Features

### Current
- Text-based conversation interface with voice response
- Dual persona system (Indiana Oracle + Kurt Vonnegut)
- Enhanced voice synthesis with ElevenLabs
- Oracle frame background with neon aesthetic
- Real-time WebSocket communication

### Planned Features
- **Speech-to-Text Input**: Hands-free conversation initiation
- **Computer Vision Integration**: Front-facing cameras for multimodal AI
  - Object recognition for visitor questions ("What's this I'm holding?")
  - Age detection system for adaptive responses (child vs adult tone)
- **Holographic Display System**: Particle-based avatar rendering
- **Beamforming Microphone Array**: Precise audio capture
- **Depth Camera**: Visitor detection and positioning
- **Multi-language Support**: Accessible to diverse audiences

## Security

The Oracle interface includes password protection to prevent unauthorized API usage. 

**Default Password:** `vonnegut1922`

To change the password:
1. Set `ORACLE_PASSWORD` in your `.env` file
2. Update the password in `frontend/web/oracle_interface_styled.html` (line 584)

**Important:** Always use password protection when deploying publicly to avoid unexpected API costs.

## Future ML Deployment Platforms

For the full installation with GPU-accelerated features (SadTalker, NVIDIA Audio2Face, computer vision):

### GPU Cloud Platforms
1. **RunPod** - GPU cloud with RTX 4090s, perfect for ML inference
2. **Vast.ai** - Cost-effective GPU rentals, good for development/testing
3. **Lambda Labs** - ML-focused cloud with NVIDIA partnership
4. **Paperspace Gradient** - Jupyter + deployment pipeline for ML workflows
5. **Google Cloud Platform** - Enterprise-grade with custom GPU VMs
6. **AWS EC2 G4/P4 instances** - Industry standard for production ML

### Local Hardware Setup
- **Recommended**: RTX 4090 or dual 4090 setup
- **OS**: Windows (for TouchDesigner integration)
- **RAM**: 32GB+ for large ML models
- **Storage**: NVMe SSD for fast model loading

### Deployment Strategy
- **Web Demo**: Railway/Render (current Oracle chatbot)
- **Development**: Local machine with 4090
- **Production Installation**: **RunPod** (chosen for GPU cloud deployment)

## RunPod Deployment (Selected Platform)

**Why RunPod:**
- Pre-configured for AI workloads (Audio2Face, SadTalker ready)
- RTX 4090 availability at $0.74/hour
- Native WebSocket support for real-time streaming
- Serverless option - pay only when visitors are talking
- Perfect for audio-to-audio pipeline with GPU acceleration

**Audio-to-Audio Pipeline on RunPod:**
```python
# Yes, audio-to-audio will work perfectly on RunPod:
# Visitor speaks → Microphone → Speech-to-Text → AI Response → TTS → Avatar Animation
# All GPU-accelerated for minimal latency
```

### Current Feature Status
- **Text Input**: ✅ Working (type questions)
- **Voice Output**: ✅ Working (ElevenLabs TTS)
- **Voice Input**: ⏳ Not yet implemented (planned for RunPod deployment)
- **Real-time Avatar**: ⏳ Future (Audio2Face/SadTalker on RunPod)

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env
# Edit .env with your API keys

# Start the Oracle server
python test_conversation_interface.py

# Access the interface at http://localhost:8500
# Enter password: vonnegut1922
```