# FastAPI REST API

A simple REST API built with FastAPI for deployment on Hetzner using Coolify.

## Features

- RESTful API with CRUD operations
- Interactive API documentation via Swagger UI
- In-memory database for demonstration
- Docker and Docker Compose support with robust port handling
- Easy deployment to Coolify
- Automated test script for API validation

## Local Development

### Windows Setup (Easiest Method)

1. Simply run the setup script:

```bash
setup_dev.bat
```

2. Run the application:

```bash
python run_dev.py
```

### Manual Setup

1. Clone this repository
2. Create and activate a virtual environment:

```bash
# Create virtual environment
python -m venv venv

# Activate on Windows
venv\Scripts\activate

# Activate on macOS/Linux
source venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run the application:

```bash
# Using the development script (with auto-reload)
python run_dev.py

# Or using uvicorn directly
uvicorn main:app --reload
```

### Using Docker

```bash
# Build and run with Docker (automatic port selection if 8000 is used)
docker build -t fastapi-app .
docker run -p 8080:8000 -e PORT=8000 fastapi-app

# Or use Docker Compose with our helper script (Windows)
deploy_docker.bat

# Or manually with Docker Compose
docker-compose up -d
```

The API uses intelligent port handling - if the specified port is in use, it will automatically try to find another available port.

## Testing the API

A test script is included to validate all API endpoints. To run the tests:

```bash
# Using the batch file (Windows)
test_api.bat

# Or directly using Python
python test_api.py
```

To test against a deployed API, specify the base URL:

```bash
# Windows batch file
test_api.bat https://your-api-url.com

# Or directly with Python
python test_api.py https://your-api-url.com
```

## API Endpoints

The API will be available at http://localhost:8000 and the interactive docs at http://localhost:8000/docs

- `GET /`: Welcome message
- `GET /items`: List all items
- `POST /items`: Create a new item
- `GET /items/{item_id}`: Get an item by ID
- `PUT /items/{item_id}`: Update an item
- `DELETE /items/{item_id}`: Delete an item
- `GET /health`: Health check endpoint

## Deployment with Coolify

1. Push your code to a Git repository
2. Log in to your Coolify instance
3. Add a new service:
   - Select "Application" and then your Git repository
   - Choose "Python" as the template
   - Set build command: `pip install -r requirements.txt`
   - Set start command: `uvicorn main:app --host 0.0.0.0 --port 80`
   - Deploy the application

For detailed deployment instructions, see [DEPLOY_COOLIFY.md](DEPLOY_COOLIFY.md).

### Automatic Configuration

This repository includes a `.coolify.yaml` file that automates the configuration process. Coolify will detect this file and configure the deployment automatically.

## Testing the Deployment

After deployment, you can access your API at the URL assigned by Coolify. The interactive API documentation will be available at `/docs`.

Example request using curl:

```bash
# List all items
curl -X GET https://your-coolify-url.com/items

# Create a new item
curl -X POST https://your-coolify-url.com/items \
  -H "Content-Type: application/json" \
  -d '{"name": "Example Item", "price": 19.99, "description": "This is an example item"}'
``` 