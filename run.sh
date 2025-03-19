#!/bin/bash
# Application entry point with error handling

# Function to log messages
log() {
  echo "[$(date +'%Y-%m-%d %H:%M:%S')] $1"
}

# Error handling
set -e
trap 'log "ERROR: Command failed with exit code $? at line $LINENO"' ERR

# Log startup
log "Starting application..."

# Check environment
log "Environment check:"
log "Working directory: $(pwd)"
log "Python version: $(python --version 2>&1)"

# Check if app directory exists
if [ ! -d "./app" ]; then
  log "ERROR: app directory not found!"
  ls -la
  exit 1
fi

# Check if main.py exists
if [ ! -f "./app/main.py" ]; then
  log "ERROR: app/main.py not found!"
  ls -la ./app
  exit 1
fi

# Get PORT from environment or use default
PORT="${PORT:-3000}"
log "Using port: $PORT"

# Try to start the application
log "Starting FastAPI application with uvicorn..."
python start.py 