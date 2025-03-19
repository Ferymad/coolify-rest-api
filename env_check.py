#!/usr/bin/env python
"""
Environment diagnostic script for troubleshooting deployment issues.
"""
import os
import sys
import socket
import platform
import traceback
from pathlib import Path

def print_header(title):
    """Print a section header."""
    print("\n" + "=" * 60)
    print(f" {title}")
    print("=" * 60)

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
    
    # Check for Coolify-specific variables
    coolify_vars = [var for var in os.environ if "COOLIFY" in var.upper()]
    if coolify_vars:
        print("Coolify environment detected!")
        for var in coolify_vars:
            value = os.environ.get(var)
            if "PASSWORD" in var.upper() or "SECRET" in var.upper() or "TOKEN" in var.upper():
                value = "*" * len(value)  # Mask sensitive values
            print(f"  {var}: {value}")
    else:
        print("No Coolify environment variables detected.")
    
    print("\nRequired Variables:")
    for var in required_vars:
        value = os.environ.get(var, "NOT SET")
        if var == "POSTGRES_PASSWORD" and value != "NOT SET":
            value = "*" * len(value)  # Mask password
        print(f"{var}: {value}")
    
    print("\nAll Environment Variables:")
    for key, value in sorted(os.environ.items()):
        if key not in ['PATH', 'PYTHONPATH'] and not key.startswith('_'):
            if 'PASSWORD' in key.upper() or 'SECRET' in key.upper() or 'TOKEN' in key.upper():
                value = "*" * len(value)  # Mask sensitive values
            print(f"  {key}: {value}")

def check_system_info():
    """Check system information."""
    print_header("SYSTEM INFORMATION")
    print(f"Python version: {sys.version}")
    print(f"Platform: {platform.platform()}")
    print(f"Processor: {platform.processor()}")
    print(f"Architecture: {platform.architecture()}")
    print(f"Node: {platform.node()}")
    
    # Check if we're running in Docker
    in_docker = os.path.exists('/.dockerenv')
    print(f"Running in Docker: {in_docker}")
    
    # Check available system resources
    try:
        import psutil
        print(f"\nCPU cores: {psutil.cpu_count()}")
        print(f"Memory available: {psutil.virtual_memory().available / (1024 * 1024):.2f} MB")
        print(f"Disk space available: {psutil.disk_usage('/').free / (1024 * 1024 * 1024):.2f} GB")
    except ImportError:
        print("\npsutil not available for resource checks")

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
    
    # List all network interfaces
    try:
        import netifaces
        print("\nNetwork Interfaces:")
        for iface in netifaces.interfaces():
            try:
                addrs = netifaces.ifaddresses(iface)
                if netifaces.AF_INET in addrs:
                    for addr in addrs[netifaces.AF_INET]:
                        print(f"  {iface}: {addr['addr']}")
            except:
                pass
    except ImportError:
        print("\nnetifaces not available for interface listing")
    
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
    
    # Try alternate hosts that might be used in Docker/Coolify environments
    alternate_hosts = ["host.docker.internal", "postgres.coolify", "localhost", "127.0.0.1"]
    for host in alternate_hosts:
        if host != postgres_host:  # Skip if it's the same as we already checked
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.settimeout(1)
                    result = s.connect_ex((host, postgres_port))
                    if result == 0:
                        print(f"Connection to alternate host {host}:{postgres_port} successful")
                    else:
                        print(f"Connection to alternate host {host}:{postgres_port} failed (error code: {result})")
            except Exception as e:
                print(f"Error checking connection to {host}: {e}")

def check_file_structure():
    """Check the file structure."""
    print_header("FILE STRUCTURE")
    
    # Check current directory
    current_dir = Path.cwd()
    print(f"Current directory: {current_dir}")
    
    # Check if entrypoint.sh exists and is executable
    entrypoint = Path("/app/entrypoint.sh")
    if entrypoint.exists():
        print(f"Entrypoint script exists: {entrypoint}")
        is_executable = os.access(entrypoint, os.X_OK)
        print(f"Entrypoint is executable: {is_executable}")
    else:
        print(f"WARNING: Entrypoint script not found at {entrypoint}")
        # Try to find it elsewhere
        for path in [Path("./entrypoint.sh"), Path("entrypoint.sh")]:
            if path.exists():
                print(f"Found entrypoint at: {path.absolute()}")
                is_executable = os.access(path, os.X_OK)
                print(f"  Is executable: {is_executable}")
    
    # List the root directory
    print("\nRoot directory content:")
    for item in Path("/").iterdir():
        if item.is_dir():
            print(f"  DIR: {item}")
        else:
            print(f"  FILE: {item}")
    
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
        "Dockerfile",
        "entrypoint.sh"
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
            if "entrypoint" in file_path:
                is_executable = os.access(path, os.X_OK)
                print(f"    Is executable: {is_executable}")
        else:
            print(f"  ✗ {file_path} (not found)")

if __name__ == "__main__":
    print_header("ENVIRONMENT DIAGNOSTIC REPORT")
    print("This script helps troubleshoot deployment issues.")
    
    try:
        check_system_info()
        check_environment_variables()
        check_network_info()
        check_file_structure()
        
        print_header("DIAGNOSTIC COMPLETE")
        print("If you see any issues above, please address them before deployment.")
    except Exception as e:
        print_header("ERROR DURING DIAGNOSTICS")
        print(f"An error occurred while running diagnostics: {e}")
        print("\nStacktrace:")
        traceback.print_exc() 