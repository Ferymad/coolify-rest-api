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

# Create dedicated entrypoint script file first
COPY entrypoint.sh /app/
RUN chmod +x /app/entrypoint.sh

# Copy application code
COPY . .

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=3000

# Make sure Python scripts are executable
RUN chmod +x env_check.py

# Expose the port
EXPOSE 3000

# Use ENTRYPOINT instead of CMD for better Coolify compatibility
ENTRYPOINT ["/app/entrypoint.sh"] 