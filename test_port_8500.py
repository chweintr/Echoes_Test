import socket
import requests
import time

# Test if port 8500 is open
def test_port():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('127.0.0.1', 8500))
    sock.close()
    
    if result == 0:
        print("Port 8500 is OPEN")
        return True
    else:
        print("Port 8500 is CLOSED")
        return False

# Test HTTP connection
def test_http():
    try:
        response = requests.get('http://localhost:8500', timeout=2)
        print(f"HTTP response: {response.status_code}")
        return True
    except Exception as e:
        print(f"HTTP error: {e}")
        return False

print("Testing port 8500...")
test_port()

print("\nTesting HTTP connection...")
test_http()

print("\nMake sure to run: python test_conversation_interface.py")
print("in a separate terminal first!")