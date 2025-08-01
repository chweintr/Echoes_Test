#!/usr/bin/env python3
"""
Indiana Oracle - Complete System Startup
Handles all setup, checks, and service management
"""

import sys
import asyncio
import subprocess
import webbrowser
import time
from pathlib import Path

# Import our utilities
from utils.enhanced_port_checker import PortManager

async def startup_sequence():
    """Complete startup sequence for Indiana Oracle"""
    
    print("""
╔══════════════════════════════════════════════════════╗
║              INDIANA ORACLE ENTITY PROJECT           ║
║                                                      ║
║   "Connecting visitors with Indiana's remarkable     ║
║    past, present, and possible futures"              ║
╚══════════════════════════════════════════════════════╝
    """)
    
    # Step 1: Port Management
    print("🔌 STEP 1: Port Management")
    port_mgr = PortManager()
    port_results = port_mgr.check_all_ports()
    
    if not all(port_results.values()):
        print("⚠️  Some ports are blocked. Attempting to free them...")
        if not port_mgr.free_all_ports():
            print("❌ Could not free required ports")
            print("Try running: python utils/enhanced_port_checker.py kill")
            return False
    
    # Step 2: Check API Keys (basic check)
    print("\n🔑 STEP 2: Configuration Check")
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    
    api_keys = {
        'OPENAI_API_KEY': os.getenv('OPENAI_API_KEY'),
        'ELEVENLABS_API_KEY': os.getenv('ELEVENLABS_API_KEY'),
        'HEYGEN_API_KEY': os.getenv('HEYGEN_API_KEY')
    }
    
    missing_keys = [k for k, v in api_keys.items() if not v]
    
    if missing_keys:
        print(f"⚠️  Missing API keys: {', '.join(missing_keys)}")
        print("System will run with limited functionality")
    else:
        print("✅ All API keys configured")
    
    # Step 3: Start Services
    print("\n🚀 STEP 3: Starting Services")
    
    services = []
    
    # Start FastAP backend
    print("Starting FastAPI backend...")
    backend_proc = subprocess.Popen([
        sys.executable, "-m", "uvicorn",
        "backend.main_oracle:app",
        "--host", "0.0.0.0",
        "--port", "8000",
        "--reload"
    ], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    services.append(("FastAPI Backend", backend_proc))
    print("✅ FastAPI backend started on port 8000")
    
    # Give backend time to start
    await asyncio.sleep(3)
    
    # Start web server for frontend
    print("Starting web interface...")
    web_proc = subprocess.Popen([
        sys.executable, "-m", "http.server", "8080",
        "--directory", "frontend/web"
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    services.append(("Web Server", web_proc))
    print("✅ Web server started on port 8080")
    
    # Start Redis (optional)
    try:
        redis_proc = subprocess.Popen(
            ["redis-server", "--port", "6379"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        services.append(("Redis", redis_proc))
        print("✅ Redis cache started on port 6379")
    except FileNotFoundError:
        print("⚠️  Redis not found - using memory cache")
    
    # Give servers time to fully start
    await asyncio.sleep(2)
    
    print(f"\n🎉 INDIANA ORACLE SYSTEM READY!")
    print("=" * 55)
    print("🌐 Oracle Interface: http://localhost:8080/oracle_interface.html")
    print("📊 API Documentation: http://localhost:8000/docs")
    print("🧪 API Test Tool: http://localhost:8000/redoc")
    print("=" * 55)
    print("Available Personas:")
    print("• Indiana Oracle (default) - The spirit of Indiana")
    print("• Kurt Vonnegut - Indianapolis novelist")
    print("• Larry Bird - The Hick from French Lick") 
    print("• David Letterman - Late night legend")
    print("• Alfred Kinsey - IU researcher")
    print("• Lil Bub - Bloomington's magical space cat")
    print("• ... and 9 more Indiana icons")
    print("=" * 55)
    
    # Auto-open browser
    try:
        webbrowser.open("http://localhost:8080/oracle_interface.html")
        print("🌐 Opened Oracle interface in browser")
    except:
        print("⚠️  Could not auto-open browser")
    
    print("\nPress Ctrl+C to stop all services")
    print("System logs will appear below...")
    print("-" * 55)
    
    try:
        # Keep services running and monitor
        while True:
            await asyncio.sleep(5)
            
            # Check if any critical service died
            for name, proc in services:
                if proc.poll() is not None and name in ["FastAPI Backend", "Web Server"]:
                    print(f"⚠️  {name} process ended unexpectedly (exit code: {proc.poll()})")
                    if name == "FastAPI Backend":
                        print("❌ Critical service failed - system unstable")
                        break
                    
    except KeyboardInterrupt:
        print("\n🛑 Shutting down Indiana Oracle...")
        
        # Graceful shutdown
        for name, proc in services:
            try:
                print(f"Stopping {name}...")
                proc.terminate()
                
                # Wait for graceful shutdown
                try:
                    proc.wait(timeout=5)
                    print(f"✅ {name} stopped gracefully")
                except subprocess.TimeoutExpired:
                    print(f"🔪 Force-killing {name}...")
                    proc.kill()
                    proc.wait()
                    
            except Exception as e:
                print(f"⚠️  Error stopping {name}: {e}")
        
        print("👋 Goodbye! So it goes.")

def quick_test():
    """Quick system test without starting servers"""
    print("Testing Indiana Oracle System...\n")
    
    # Test imports
    try:
        import fastapi, uvicorn, websockets, aiohttp
        print("[OK] Core packages available")
    except ImportError as e:
        print(f"[ERROR] Missing package: {e}")
        return False
    
    # Test ports
    port_mgr = PortManager()
    results = port_mgr.check_all_ports()
    
    available_count = sum(results.values())
    total_ports = len(results)
    
    if available_count == total_ports:
        print("[OK] All ports available")
        return True
    else:
        print(f"[WARNING] {total_ports - available_count} ports blocked")
        return False

def main():
    """Main entry point"""
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == 'test':
            quick_test()
        elif command == 'ports':
            port_mgr = PortManager()
            port_mgr.check_all_ports()
        elif command == 'kill-ports':
            port_mgr = PortManager()
            port_mgr.check_all_ports(auto_kill=True)
        else:
            print("Usage:")
            print("  python start_indiana_oracle.py          # Start full system")
            print("  python start_indiana_oracle.py test     # Quick system test")
            print("  python start_indiana_oracle.py ports    # Check port status")
            print("  python start_indiana_oracle.py kill-ports # Free blocked ports")
    else:
        # Full startup
        try:
            asyncio.run(startup_sequence())
        except KeyboardInterrupt:
            print("\nStartup cancelled")


if __name__ == "__main__":
    main()