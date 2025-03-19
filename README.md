# FastAPI REST API

A simple REST API built with FastAPI for deployment on Hetzner using Coolify.

## Features

- RESTful API with CRUD operations
- Interactive API documentation via Swagger UI
- PostgreSQL database with Tortoise ORM
- Docker and Docker Compose support with automatic port detection
- Easy deployment to Coolify

## Quick Start

### Local Development

```bash
# Setup and activate virtual environment on Windows
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# Run the application
python start.py
```

### Docker

```bash
# Using Docker Compose (recommended)
docker-compose up -d

# Using Docker directly
docker build -t fastapi-app .
docker run -p 8080:8000 -e PORT=8000 fastapi-app
```

## API Endpoints

- `GET /`: Welcome message
- `GET /items`: List all items
- `POST /items`: Create a new item
- `GET /items/{item_id}`: Get an item by ID
- `PUT /items/{item_id}`: Update an item
- `DELETE /items/{item_id}`: Delete an item
- `GET /health`: Health check endpoint

API documentation available at: `/docs`

## Environment Variables

The application uses the following environment variables:

```env
# API configuration
API_PORT=8080
PORT=8000

# Database configuration
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=mydb
POSTGRES_PORT=5432
POSTGRES_HOST=postgres

# App configuration
APP_NAME=FastAPI REST API with Tortoise ORM
APP_VERSION=1.0.0
APP_DESCRIPTION=A RESTful API built with FastAPI and Tortoise ORM for deployment on Hetzner with Coolify
```

## Deployment

1. Push code to a Git repository
2. Set up Coolify on your Hetzner server
3. Add a new service in Coolify linked to your repository
4. Configure environment variables in Coolify
5. Deploy the application

For detailed deployment instructions, see [DEPLOY_COOLIFY.md](DEPLOY_COOLIFY.md). 