"""
Main application entry point for the FastAPI REST API with Tortoise ORM.
"""
import os
import sys
from fastapi import FastAPI
from loguru import logger
from contextlib import asynccontextmanager

from app.config import openapi_config
from app.initializer import init

# Configure logger for better output
logger.remove()
logger.add(sys.stderr, level="INFO", format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | <cyan>{module}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>")

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan context manager for startup and shutdown events.
    
    Args:
        app: The FastAPI application instance.
    """
    try:
        # Startup logic
        logger.info("Starting application...")
        logger.info(f"POSTGRES_HOST: {os.environ.get('POSTGRES_HOST', 'not set')}")
        logger.info(f"POSTGRES_PORT: {os.environ.get('POSTGRES_PORT', 'not set')}")
        logger.info(f"POSTGRES_DB: {os.environ.get('POSTGRES_DB', 'not set')}")
        logger.info(f"Working directory: {os.getcwd()}")
        yield
    except Exception as e:
        logger.error(f"Error during startup: {e}")
        raise
    finally:
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
    logger.info("Root endpoint accessed")
    return {
        "message": "Welcome to the FastAPI REST API with Tortoise ORM",
        "status": "online",
        "documentation": "/docs"
    }

@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint for monitoring."""
    logger.info("Health check endpoint accessed")
    return {"status": "healthy"}

try:
    # Initialize the application
    logger.info("Starting application initialization...")
    init(app)
except Exception as e:
    logger.error(f"Failed to initialize application: {e}")
    raise 