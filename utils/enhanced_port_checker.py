"""
Enhanced Port Management for Indiana Oracle
Automatically handles port conflicts and process management
"""

import socket
import subprocess
import sys
import psutil
from typing import Dict, List, Optional

class PortManager:
    def __init__(self):
        self.required_ports = {
            8000: "FastAPI Main Server",
            8001: "WebSocket Server", 
            8002: "HeyGen WebRTC",
            9001: "TouchDesigner Bridge",
            9002: "Spout Video Server",
            6379: "Redis Cache",
            3000: "Frontend Development"
        }
    
    def check_port_available(self, port: int) -> bool:
        """Check if a port is available"""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            result = sock.connect_ex(('127.0.0.1', port))
            return result != 0
    
    def get_process_on_port(self, port: int) -> Optional[Dict]:
        """Get detailed process info for a port"""
        for conn in psutil.net_connections():
            if conn.laddr.port == port:
                try:
                    process = psutil.Process(conn.pid)
                    return {
                        'pid': conn.pid,
                        'name': process.name(),
                        'exe': process.exe(),
                        'cmdline': ' '.join(process.cmdline())
                    }
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
        return None
    
    def kill_process_on_port(self, port: int, force: bool = False) -> bool:
        """Kill process using a specific port"""
        process_info = self.get_process_on_port(port)
        if not process_info:
            return False
        
        try:
            process = psutil.Process(process_info['pid'])
            
            if not force:
                # Ask user for confirmation
                print(f"\nProcess using port {port}:")
                print(f"  Name: {process_info['name']}")
                print(f"  PID: {process_info['pid']}")
                print(f"  Command: {process_info['cmdline']}")
                
                choice = input(f"Kill this process? (y/N): ").strip().lower()
                if choice != 'y':
                    return False
            
            # Try graceful termination first
            process.terminate()
            
            # Wait for process to end
            try:
                process.wait(timeout=5)
                print(f"[OK] Process {process_info['pid']} terminated gracefully")
                return True
            except psutil.TimeoutExpired:
                # Force kill if needed
                process.kill()
                print(f"[OK] Process {process_info['pid']} force-killed")
                return True
                
        except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
            print(f"[ERROR] Could not kill process: {e}")
            return False
    
    def check_all_ports(self, auto_kill: bool = False) -> Dict[int, bool]:
        """Check all required ports and optionally kill blocking processes"""
        results = {}
        
        print("Checking required ports for Indiana Oracle...\n")
        
        for port, service in self.required_ports.items():
            if self.check_port_available(port):
                print(f"[OK] Port {port} ({service}) - Available")
                results[port] = True
            else:
                print(f"[BLOCKED] Port {port} ({service}) - IN USE")
                
                if auto_kill:
                    if self.kill_process_on_port(port, force=True):
                        results[port] = True
                        print(f"   ↳ Process killed, port now available")
                    else:
                        results[port] = False
                        print(f"   ↳ Could not free port")
                else:
                    process_info = self.get_process_on_port(port)
                    if process_info:
                        print(f"   ↳ Process: {process_info['name']} (PID: {process_info['pid']})")
                        print(f"   ↳ Command: {process_info['cmdline']}")
                    results[port] = False
        
        return results
    
    def free_all_ports(self):
        """Interactive port cleanup"""
        blocked_ports = []
        
        for port, service in self.required_ports.items():
            if not self.check_port_available(port):
                blocked_ports.append(port)
        
        if not blocked_ports:
            print("[OK] All ports are available!")
            return True
        
        print(f"\n[WARNING] {len(blocked_ports)} ports are blocked")
        print("Options:")
        print("1. Kill all blocking processes (automatic)")
        print("2. Kill processes one by one (interactive)")
        print("3. Show process details only")
        print("4. Cancel")
        
        choice = input("Choose option (1-4): ").strip()
        
        if choice == '1':
            success_count = 0
            for port in blocked_ports:
                if self.kill_process_on_port(port, force=True):
                    success_count += 1
            
            print(f"\n[OK] Freed {success_count}/{len(blocked_ports)} ports")
            return success_count == len(blocked_ports)
        
        elif choice == '2':
            for port in blocked_ports:
                service = self.required_ports[port]
                print(f"\n🔍 Port {port} ({service}):")
                self.kill_process_on_port(port, force=False)
        
        elif choice == '3':
            for port in blocked_ports:
                process_info = self.get_process_on_port(port)
                if process_info:
                    print(f"\nPort {port}: {process_info['name']} (PID: {process_info['pid']})")
                    print(f"  Command: {process_info['cmdline']}")
        
        return False


def main():
    """Command line interface for port management"""
    port_mgr = PortManager()
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == 'check':
            port_mgr.check_all_ports()
        elif command == 'kill':
            port_mgr.check_all_ports(auto_kill=True)
        elif command == 'free':
            port_mgr.free_all_ports()
        else:
            print("Usage: python enhanced_port_checker.py [check|kill|free]")
    else:
        # Interactive mode
        port_mgr.free_all_ports()


if __name__ == "__main__":
    main()