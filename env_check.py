#!/usr/bin/env python
"""
Environment diagnostic script for troubleshooting deployment issues.
"""
import os
import sys
import socket
import platform
from pathlib import Path

def print_header(title):
    """Print a section header."""
    print("\n" + "=" * 40)
    print(f" {title}")
    print("=" * 40)

def check_environment_variables():
    """Check all environment variables."""
    print_header("ENVIRONMENT VARIABLES")
    
    required_vars = [
        "PORT",
        "POSTGRES_USER", 
        "POSTGRES_PASSWORD", 
        "POSTGRES_DB", 
        "POSTGRES_PORT", 
        "POSTGRES_HOST"
    ]
    
    for var in required_vars:
        value = os.environ.get(var, "NOT SET")
        if var == "POSTGRES_PASSWORD" and value != "NOT SET":
            value = "*" * len(value)  # Mask password
        print(f"{var}: {value}")
    
    print("\nAll Environment Variables:")
    for key, value in sorted(os.environ.items()):
        if key not in ['PATH', 'PYTHONPATH'] and not key.startswith('_'):
            if 'PASSWORD' in key:
                value = "*" * len(value)  # Mask password
            print(f"  {key}: {value}")

def check_system_info():
    """Check system information."""
    print_header("SYSTEM INFORMATION")
    print(f"Python version: {sys.version}")
    print(f"Platform: {platform.platform()}")
    print(f"Processor: {platform.processor()}")
    print(f"Architecture: {platform.architecture()}")
    print(f"Node: {platform.node()}")

def check_network_info():
    """Check network information."""
    print_header("NETWORK INFORMATION")
    hostname = socket.gethostname()
    print(f"Hostname: {hostname}")
    try:
        ip = socket.gethostbyname(hostname)
        print(f"IP Address: {ip}")
    except socket.gaierror:
        print("Could not determine IP address")
    
    # Check if postgres host is reachable
    postgres_host = os.environ.get("POSTGRES_HOST", "postgres")
    postgres_port = int(os.environ.get("POSTGRES_PORT", "5432"))
    
    print(f"\nChecking connection to {postgres_host}:{postgres_port}...")
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(3)
            result = s.connect_ex((postgres_host, postgres_port))
            if result == 0:
                print(f"Connection to {postgres_host}:{postgres_port} successful")
            else:
                print(f"Connection to {postgres_host}:{postgres_port} failed (error code: {result})")
    except Exception as e:
        print(f"Error checking connection: {e}")

def check_file_structure():
    """Check the file structure."""
    print_header("FILE STRUCTURE")
    
    # Check current directory
    current_dir = Path.cwd()
    print(f"Current directory: {current_dir}")
    
    # Key directories to check
    dirs_to_check = [
        "app",
        "app/core",
        "app/config",
        "app/core/models",
        "app/core/routers"
    ]
    
    # Key files to check
    files_to_check = [
        "app/main.py",
        "app/initializer.py",
        "app/config/db.py",
        "app/core/models/tortoise/__init__.py",
        "app/core/models/pydantic/__init__.py",
        "app/core/routers/items.py",
        ".env",
        "requirements.txt",
        "Dockerfile"
    ]
    
    print("\nChecking directories:")
    for dir_path in dirs_to_check:
        path = current_dir / dir_path
        if path.exists() and path.is_dir():
            print(f"  ✓ {dir_path}")
        else:
            print(f"  ✗ {dir_path} (not found)")
    
    print("\nChecking files:")
    for file_path in files_to_check:
        path = current_dir / file_path
        if path.exists() and path.is_file():
            print(f"  ✓ {file_path}")
        else:
            print(f"  ✗ {file_path} (not found)")

if __name__ == "__main__":
    print_header("ENVIRONMENT DIAGNOSTIC REPORT")
    print("This script helps troubleshoot deployment issues.")
    
    check_system_info()
    check_environment_variables()
    check_network_info()
    check_file_structure()
    
    print_header("DIAGNOSTIC COMPLETE")
    print("If you see any issues above, please address them before deployment.") 