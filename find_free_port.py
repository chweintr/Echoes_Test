import socket

def find_free_port(start=8500, end=9000):
    """Find a free port in the given range"""
    for port in range(start, end):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            result = sock.connect_ex(('127.0.0.1', port))
            if result != 0:
                print(f"Port {port} is available")
                return port
    return None

# Test common ports
test_ports = [7080, 7081, 8000, 8080, 8081, 8765, 8766, 8767, 9080, 9081]
print("Checking common ports:")
for port in test_ports:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        result = sock.connect_ex(('127.0.0.1', port))
        if result == 0:
            print(f"Port {port}: IN USE")
        else:
            print(f"Port {port}: Available")

print("\nFinding free port in range 8500-9000:")
free_port = find_free_port()
print(f"Recommended port: {free_port}")