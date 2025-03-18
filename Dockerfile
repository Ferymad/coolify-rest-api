FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8000

# Expose the port from the environment variable
EXPOSE $PORT

# Command to run in production - use port-aware script
CMD ["python", "start.py"]

# For development with auto-reload, override with:
# CMD ["python", "run_dev.py"] 