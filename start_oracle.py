#!/usr/bin/env python3
"""
Indiana Oracle Entity Project - Main Launcher
Starts all necessary services for the Oracle installation
"""

import asyncio
import subprocess
import sys
import os
import webbrowser
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class OracleLauncher:
    def __init__(self):
        self.processes = []
        self.base_dir = Path(__file__).parent
        
    def check_requirements(self):
        """Check if all required packages are installed"""
        required = [
            'fastapi',
            'uvicorn',
            'websockets',
            'openai',
            'elevenlabs',
            'aiohttp',
            'numpy',
            'torch'
        ]
        
        missing = []
        for package in required:
            try:
                __import__(package)
            except ImportError:
                missing.append(package)
        
        if missing:
            logger.error(f"Missing packages: {', '.join(missing)}")
            logger.info("Installing missing packages...")
            subprocess.check_call([
                sys.executable, '-m', 'pip', 'install', *missing
            ])
        
        return True
    
    def check_environment(self):
        """Check environment variables"""
        warnings = []
        
        if not os.getenv('OPENAI_API_KEY'):
            warnings.append("OPENAI_API_KEY not set - AI responses will be limited")
        
        if not os.getenv('ELEVENLABS_API_KEY'):
            warnings.append("ELEVENLABS_API_KEY not set - using local TTS")
        
        if not os.getenv('HEYGEN_API_KEY'):
            warnings.append("HEYGEN_API_KEY not set - avatar features disabled")
        
        for warning in warnings:
            logger.warning(warning)
        
        return len(warnings) == 0
    
    async def start_backend(self):
        """Start the FastAPI backend server"""
        logger.info("Starting Oracle backend server...")
        
        cmd = [
            sys.executable,
            str(self.base_dir / "backend" / "main_oracle.py")
        ]
        
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        self.processes.append(process)
        logger.info("Backend server started on http://localhost:8000")
        
        return process
    
    async def start_web_interface(self):
        """Start web interface server"""
        logger.info("Starting web interface...")
        
        # Simple HTTP server for the frontend
        cmd = [
            sys.executable,
            '-m',
            'http.server',
            '8080',
            '--directory',
            str(self.base_dir / "frontend" / "web")
        ]
        
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        self.processes.append(process)
        logger.info("Web interface available at http://localhost:8080")
        
        return process
    
    def open_browser(self):
        """Open the Oracle interface in browser"""
        import time
        time.sleep(3)  # Wait for servers to start
        
        url = "http://localhost:8080/oracle_interface.html"
        webbrowser.open(url)
        logger.info(f"Opened browser: {url}")
    
    async def monitor_processes(self):
        """Monitor running processes"""
        while True:
            for i, process in enumerate(self.processes):
                if process.returncode is not None:
                    logger.error(f"Process {i} exited with code {process.returncode}")
            
            await asyncio.sleep(5)
    
    async def shutdown(self):
        """Gracefully shutdown all processes"""
        logger.info("Shutting down Oracle system...")
        
        for process in self.processes:
            try:
                process.terminate()
                await process.wait()
            except:
                pass
        
        logger.info("Shutdown complete")
    
    async def run(self):
        """Main run method"""
        logger.info("""
╔═══════════════════════════════════════════════════════════╗
║           INDIANA ORACLE ENTITY PROJECT                   ║
║                                                           ║
║   Connecting visitors with Indiana's remarkable past,     ║
║   present, and possible futures through AI avatars        ║
╚═══════════════════════════════════════════════════════════╝
        """)
        
        # Check requirements
        if not self.check_requirements():
            return
        
        # Check environment
        self.check_environment()
        
        try:
            # Start services
            await self.start_backend()
            await self.start_web_interface()
            
            # Open browser
            asyncio.create_task(asyncio.to_thread(self.open_browser))
            
            logger.info("""
═══════════════════════════════════════════════════════════════
System Ready! 

Available personas:
- Indiana Oracle (Main)
- Kurt Vonnegut
- Larry Bird  
- David Letterman
- ... and more

Access the interface at: http://localhost:8080/oracle_interface.html

Press Ctrl+C to stop
═══════════════════════════════════════════════════════════════
            """)
            
            # Monitor processes
            await self.monitor_processes()
            
        except KeyboardInterrupt:
            logger.info("\nReceived shutdown signal")
        except Exception as e:
            logger.error(f"Error: {e}")
        finally:
            await self.shutdown()


def main():
    """Entry point"""
    launcher = OracleLauncher()
    
    try:
        asyncio.run(launcher.run())
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()