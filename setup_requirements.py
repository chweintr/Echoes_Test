#!/usr/bin/env python3
"""
Indiana Oracle - Dependency Setup
Installs all required packages with error handling
"""

import subprocess
import sys
import os
import importlib
from pathlib import Path

def install_package(package, description=""):
    """Install a single package with error handling"""
    try:
        print(f"Installing {package}... ", end="", flush=True)
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", package],
            capture_output=True,
            text=True,
            timeout=120
        )
        
        if result.returncode == 0:
            print("✅")
            return True
        else:
            print(f"❌ ({result.stderr.strip()})")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ (timeout)")
        return False
    except Exception as e:
        print(f"❌ ({e})")
        return False

def check_package(package):
    """Check if a package is already installed"""
    try:
        importlib.import_module(package.replace('-', '_'))
        return True
    except ImportError:
        return False

def setup_environment():
    """Set up Python environment and install packages"""
    
    print("""
╔════════════════════════════════════════════════════╗
║         INDIANA ORACLE DEPENDENCY SETUP           ║
╚════════════════════════════════════════════════════╝
    """)
    
    # Check Python version
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ required")
        return False
    
    print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
    
    # Upgrade pip first
    print("\n📦 Upgrading pip...")
    subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], 
                  capture_output=True)
    
    # Core packages (required)
    core_packages = [
        ("fastapi", "Web framework"),
        ("uvicorn[standard]", "ASGI server"),
        ("websockets", "WebSocket support"),
        ("aiohttp", "Async HTTP client"),
        ("python-multipart", "Form data parsing"),
        ("python-dotenv", "Environment variables"),
        ("pydantic", "Data validation"),
        ("pydantic-settings", "Settings management"),
    ]
    
    # AI/ML packages
    ai_packages = [
        ("openai", "OpenAI API client"),
        ("elevenlabs", "ElevenLabs TTS"),
        ("anthropic", "Claude API (optional)"),
    ]
    
    # Audio processing
    audio_packages = [
        ("numpy", "Numerical computing"),
        ("scipy", "Scientific computing"),  
        ("librosa", "Audio analysis"),
        ("soundfile", "Audio file I/O"),
        ("pyttsx3", "Local TTS fallback"),
    ]
    
    # System utilities
    util_packages = [
        ("psutil", "System monitoring"),
        ("python-osc", "TouchDesigner communication"),
        ("keyring", "Secure key storage"),
        ("rich", "Pretty terminal output"),
        ("click", "CLI framework"),
    ]
    
    # Optional packages
    optional_packages = [
        ("redis", "Caching"),
        ("torch", "PyTorch (for advanced features)"),
        ("transformers", "Hugging Face models"),
        ("sentence-transformers", "Text embeddings"),
    ]
    
    all_packages = [
        ("Core", core_packages),
        ("AI/ML", ai_packages), 
        ("Audio", audio_packages),
        ("Utilities", util_packages),
        ("Optional", optional_packages)
    ]
    
    failed_packages = []
    
    for category, packages in all_packages:
        print(f"\n🔧 Installing {category} packages:")
        print("-" * 40)
        
        for package, desc in packages:
            # Check if already installed
            check_name = package.split('[')[0]  # Handle package[extras] format
            
            if check_package(check_name):
                print(f"{package} - Already installed ✅")
                continue
            
            if not install_package(package, desc):
                failed_packages.append((package, category))
                
                # For optional packages, continue
                if category == "Optional":
                    continue
                # For core packages, this is more serious
                elif category == "Core":
                    print(f"⚠️  {package} is required for basic functionality")
    
    # Summary
    print("\n" + "="*50)
    print("INSTALLATION SUMMARY")
    print("="*50)
    
    if not failed_packages:
        print("🎉 All packages installed successfully!")
        
        # Create a simple test
        print("\n🧪 Testing imports...")
        test_imports = [
            "fastapi", "uvicorn", "websockets", "aiohttp", 
            "openai", "numpy", "psutil"
        ]
        
        for module in test_imports:
            try:
                importlib.import_module(module)
                print(f"✅ {module}")
            except ImportError:
                print(f"❌ {module}")
        
        print(f"\n✅ Setup complete! Run: python start_indiana_oracle.py")
        return True
        
    else:
        print(f"⚠️  {len(failed_packages)} packages failed to install:")
        for package, category in failed_packages:
            print(f"  - {package} ({category})")
        
        print("\nTry installing failed packages manually:")
        for package, _ in failed_packages:
            print(f"  pip install {package}")
        
        return len([p for p, c in failed_packages if c != "Optional"]) == 0

def create_env_file():
    """Create .env file if it doesn't exist"""
    env_file = Path(".env")
    
    if env_file.exists():
        print("✅ .env file already exists")
        return
    
    # Copy from template
    template_file = Path(".env.template")
    if template_file.exists():
        import shutil
        shutil.copy(template_file, env_file)
        print("✅ Created .env file from template")
        print("⚠️  Please edit .env file and add your API keys")
    else:
        # Create basic .env file
        basic_env = """# Indiana Oracle Entity Project - Environment Variables

# API Keys - ADD YOUR ACTUAL KEYS HERE
OPENAI_API_KEY=your_openai_key_here
ELEVENLABS_API_KEY=your_elevenlabs_key_here
HEYGEN_API_KEY=your_heygen_key_here

# Server Configuration
SERVER_HOST=0.0.0.0
SERVER_PORT=8000
WS_PORT=8001

# Development Settings
DEBUG=true
LOG_LEVEL=INFO
"""
        
        with open(env_file, 'w') as f:
            f.write(basic_env)
        
        print("✅ Created basic .env file")
        print("⚠️  Please edit .env file and add your API keys")

def main():
    """Main setup function"""
    success = setup_environment()
    
    if success:
        create_env_file()
        
        print("""
🎉 SETUP COMPLETE!

Next steps:
1. Edit .env file and add your API keys
2. Run: python start_indiana_oracle.py
3. Open: http://localhost:8080/oracle_interface.html

For help:
- python start_indiana_oracle.py test  # Quick test
- python utils/enhanced_port_checker.py  # Check ports
- python test_apis.py  # Test API connections
        """)
    else:
        print("\n❌ Setup incomplete - please resolve package installation issues")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())