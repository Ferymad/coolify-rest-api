#!/bin/bash

echo "======================================"
echo "Running environment diagnostics..."
python env_check.py
echo "======================================"
echo "Starting FastAPI application..."
echo "Environment: PORT=$PORT"
echo "======================================"
exec python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT 