FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=3000

# Make scripts executable
RUN chmod +x run.sh check_env.sh

# Expose the port
EXPOSE 3000

# Install curl for healthcheck and netstat for diagnostics
RUN apt-get update && apt-get install -y curl net-tools && apt-get clean

# Add healthcheck
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:3000/health || exit 1

# Command to run in production
CMD ["bash", "run.sh"]

# For development with auto-reload, override with:
# CMD ["python", "run_dev.py"] 