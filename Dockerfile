FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=3000

# Create a startup script
RUN echo '#!/bin/bash\n\
echo "======================================"\n\
echo "Running environment diagnostics..."\n\
python env_check.py\n\
echo "======================================"\n\
echo "Starting FastAPI application..."\n\
echo "Environment: PORT=$PORT"\n\
echo "======================================"\n\
exec python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT\n'\
> /app/entrypoint.sh && chmod +x /app/entrypoint.sh

# Make sure Python scripts are executable
RUN chmod +x env_check.py

# Expose the port
EXPOSE 3000

# Use ENTRYPOINT instead of CMD for better Coolify compatibility
ENTRYPOINT ["/app/entrypoint.sh"] 