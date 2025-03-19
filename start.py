"""
Startup script for the FastAPI application with automatic port detection.
"""
import os
import socket
import sys
import uvicorn

def is_port_in_use(port):
    """Check if a port is in use."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

def find_available_port(start_port, max_attempts=10):
    """Find an available port starting from start_port."""
    port = start_port
    for _ in range(max_attempts):
        if not is_port_in_use(port):
            return port
        port += 1
    return None

if __name__ == "__main__":
    # Get port from environment variable or use default
    requested_port = int(os.environ.get("PORT", 8000))
    
    # If the port is in use, find an alternative
    if is_port_in_use(requested_port):
        print(f"Warning: Port {requested_port} is already in use.")
        available_port = find_available_port(requested_port + 1)
        
        if available_port:
            print(f"Using alternative port: {available_port}")
            os.environ["PORT"] = str(available_port)
            port = available_port
        else:
            print("Error: Could not find an available port. Exiting.")
            sys.exit(1)
    else:
        port = requested_port
    
    # Run the server
    uvicorn.run("main:app", host="0.0.0.0", port=port) 