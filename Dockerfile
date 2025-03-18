FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Command to run in production
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# For development with auto-reload, override with:
# CMD ["python", "run_dev.py"] 