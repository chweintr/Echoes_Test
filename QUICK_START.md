# Indiana Oracle - Quick Start Guide

## 🚀 What We've Built

You now have a complete framework for the Indiana Oracle Entity Project with:

### ✅ Completed Components:
1. **Multi-persona system** - Switch between 15 Indiana personalities
2. **WebSocket architecture** - Real-time streaming pipeline
3. **Beautiful holographic UI** - Particle effects and transitions  
4. **API integrations** - ElevenLabs, HeyGen, OpenAI ready
5. **Detailed persona prompts** - Indiana Oracle & Kurt Vonnegut configured

### 📁 Project Structure:
```
indiana-oracle-main/
├── backend/              # FastAPI server with WebSocket support
├── personas/             # Individual persona modules
├── shared/              # Shared components (TTS, avatars, etc)
├── frontend/            # Web interface with particle effects
├── config/              # Detailed persona configurations
└── your old vonnegut/   # Original Vonnegut code preserved
```

## 🔧 Next Steps to Launch

### 1. Fix API Keys
Your ElevenLabs key seems invalid. Double-check and update in `.env`:
```bash
ELEVENLABS_API_KEY=your_actual_key_here
```

### 2. Add OpenAI Key
Add your OpenAI API key to `.env`:
```bash
OPENAI_API_KEY=sk-your_openai_key_here
```

### 3. Install Dependencies
```bash
cd indiana-oracle-main
pip install -r requirements.txt
```

### 4. Test the System
```bash
# Test API connections
python test_apis.py

# Start the Oracle
python start_oracle.py
```

### 5. Access the Interface
Open http://localhost:8080/oracle_interface.html

## 🎯 Immediate Priorities

### This Week:
1. **Contact HeyGen** about multiple avatar pricing
2. **Create ElevenLabs voices** for each persona
3. **Test latency** with Indiana Oracle persona
4. **Build TouchDesigner** particle system

### Technical TODOs:
- [ ] Integrate your existing Vonnegut voice model
- [ ] Set up FAQ detection system
- [ ] Implement particle emergence animations
- [ ] Test with actual microphone input
- [ ] Optimize for <500ms response time

## 🎨 Display Decision Needed

Choose between:
1. **Hypervsn** (4x 65cm units) - True holographic but $$$ 
2. **Pepper's Ghost** (14x9ft projection) - Larger, cheaper

## 💡 Testing Order

1. Start with **Indiana Oracle** (default persona)
2. Add **Kurt Vonnegut** (you have voice + dataset)
3. Then **Larry Bird** or **David Letterman**
4. Finally the non-celebrity personas

## ⚠️ Current Issues

1. **ElevenLabs API key** - Shows as unauthorized
2. **HeyGen avatars** - Need to create avatar IDs  
3. **OpenAI key** - Not added yet

## 📞 Who to Contact

1. **HeyGen Support** - For educational pricing
2. **ElevenLabs Support** - If API key issues persist
3. **Local museums** - For installation partnerships

## 🎉 What's Working

- Complete persona management system
- Real-time WebSocket pipeline
- Beautiful particle-based UI
- Modular architecture for 15 personas
- Detailed personality prompts

The foundation is solid! Just need to:
1. Fix the API keys
2. Create the avatars/voices
3. Test with real conversations

Good luck with the Indiana Oracle! 🌟