#!/usr/bin/env python
"""
Startup script for the FastAPI application with automatic port detection.
"""
import os
import socket
import sys
import traceback
import uvicorn
from loguru import logger

def is_port_in_use(port):
    """Check if a port is in use."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex(('0.0.0.0', port)) == 0
    except Exception as e:
        logger.error(f"Error checking port {port}: {e}")
        return False

def find_available_port(start_port, max_attempts=10):
    """Find an available port starting from start_port."""
    port = start_port
    for _ in range(max_attempts):
        if not is_port_in_use(port):
            return port
        port += 1
    return None

if __name__ == "__main__":
    try:
        # Print environment for debugging
        logger.info("Environment variables:")
        for key, value in os.environ.items():
            if not key.startswith("PATH") and not key.startswith("LS_") and not key.startswith("PYTHON"):
                logger.info(f"  {key}={value}")

        # Get port from environment variable or use default
        port_str = os.environ.get("PORT", "3000")
        logger.info(f"Using PORT from environment: {port_str}")
        
        try:
            requested_port = int(port_str)
        except ValueError:
            logger.error(f"Invalid PORT value: {port_str}. Using default port 3000.")
            requested_port = 3000
        
        # If the port is in use, find an alternative
        if is_port_in_use(requested_port):
            logger.warning(f"Port {requested_port} is already in use.")
            available_port = find_available_port(requested_port + 1)
            
            if available_port:
                logger.info(f"Using alternative port: {available_port}")
                os.environ["PORT"] = str(available_port)
                port = available_port
            else:
                logger.error("Could not find an available port. Exiting.")
                sys.exit(1)
        else:
            port = requested_port
        
        # Run the server with the new app module path
        logger.info(f"Starting server on port {port}")
        logger.info(f"Working directory: {os.getcwd()}")
        logger.info(f"Files in current directory: {os.listdir('.')}")
        logger.info(f"App directory content: {os.listdir('./app') if os.path.exists('./app') else 'app directory not found'}")
        
        uvicorn.run(
            "app.main:app",
            host="0.0.0.0",
            port=port,
            log_level="info",
            reload=False
        )
    except Exception as e:
        logger.error(f"Failed to start server: {e}")
        logger.error(traceback.format_exc())
        sys.exit(1) 