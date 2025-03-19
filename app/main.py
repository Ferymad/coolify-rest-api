"""
Main application entry point for the FastAPI REST API with Tortoise ORM.
"""
from fastapi import FastAPI
from loguru import logger
from contextlib import asynccontextmanager

from app.config import openapi_config
from app.initializer import init

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan context manager for startup and shutdown events.
    
    Args:
        app: The FastAPI application instance.
    """
    # Startup logic
    logger.info("Starting application...")
    yield
    # Shutdown logic
    logger.info("Shutting down application...")

# Create FastAPI application instance
app = FastAPI(
    title=openapi_config.name,
    version=openapi_config.version,
    description=openapi_config.description,
    lifespan=lifespan,
)

@app.get("/", tags=["Root"])
async def read_root():
    """Root endpoint that returns a welcome message."""
    return {
        "message": "Welcome to the FastAPI REST API with Tortoise ORM",
        "status": "online",
        "documentation": "/docs"
    }

@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint for monitoring."""
    return {"status": "healthy"}

# Initialize the application
logger.info("Starting application initialization...")
init(app)
logger.success("Successfully initialized!") 