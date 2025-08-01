# Indiana Oracle Deployment Guide

## Quick Start (Local)

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment**:
   - Copy `.env.example` to `.env`
   - Add your API keys

3. **Add the oracle frame image**:
   - Copy your "test oracle" image to `assets/oracle-frame.webp`

4. **Run the server**:
   ```bash
   python test_conversation_interface.py
   ```

5. **Open browser**: http://localhost:8500

## Deployment Options

### Option 1: Render.com (Recommended for WebSockets)

1. **Create `render.yaml`**:
   ```yaml
   services:
     - type: web
       name: indiana-oracle
       env: python
       buildCommand: pip install -r requirements.txt
       startCommand: python test_conversation_interface.py
       envVars:
         - key: PORT
           value: 8500
   ```

2. **Deploy**:
   - Push to GitHub
   - Connect Render to your repo
   - Add environment variables in Render dashboard

### Option 2: Fly.io (Best for Real-time + Future GPU)

1. **Install Fly CLI**: https://fly.io/docs/getting-started/

2. **Create `fly.toml`**:
   ```toml
   app = "indiana-oracle"
   
   [env]
     PORT = "8500"
   
   [experimental]
     allowed_public_ports = []
     auto_rollback = true
   
   [[services]]
     http_checks = []
     internal_port = 8500
     protocol = "tcp"
     script_checks = []
   
     [[services.ports]]
       force_https = true
       handlers = ["http"]
       port = 80
   
     [[services.ports]]
       handlers = ["tls", "http"]
       port = 443
   ```

3. **Deploy**:
   ```bash
   fly launch
   fly secrets set OPENAI_API_KEY=your_key
   fly secrets set ELEVENLABS_API_KEY=your_key
   fly deploy
   ```

### Option 3: DigitalOcean App Platform

1. **Create app.yaml**:
   ```yaml
   name: indiana-oracle
   services:
   - environment_slug: python
     github:
       branch: main
       deploy_on_push: true
       repo: your-github/indiana-oracle
     http_port: 8500
     instance_count: 1
     instance_size_slug: basic-xxs
     name: oracle-backend
     run_command: python test_conversation_interface.py
   ```

## Production Considerations

### For Museum Installation

1. **Use dedicated server** with GPU support for future particle rendering
2. **Consider edge deployment** for low latency
3. **Set up monitoring** with tools like Sentry
4. **Use CDN** for static assets (oracle-frame.webp)
5. **Implement rate limiting** for public access

### Security

1. **Never commit** `.env` file
2. **Use secrets management** in production
3. **Enable CORS** only for your frontend domain
4. **Add authentication** if needed

### Performance

1. **Cache persona responses** with Redis
2. **Use connection pooling** for database
3. **Implement WebSocket heartbeat** for stability
4. **Consider load balancing** for multiple instances

## Next Steps

After basic deployment:

1. **Add speech recognition**: Web Speech API integration
2. **Implement HeyGen avatars**: Requires TURN server setup
3. **TouchDesigner integration**: OSC bridge configuration
4. **GPU particle system**: Requires GPU-enabled hosting

## Environment Variables

Required for all deployments:
- `OPENAI_API_KEY`: Your OpenAI API key
- `ELEVENLABS_API_KEY`: Your ElevenLabs API key
- `HEYGEN_API_KEY`: Your HeyGen API key (future use)
- `PORT`: Server port (default 8500)