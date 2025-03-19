"""
Main application entry point for the FastAPI REST API with Tortoise ORM.
"""
import os
import sys
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from contextlib import asynccontextmanager

from app.config import openapi_config
from app.initializer import init

# Configure logger for better output
logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}")

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan context manager for startup and shutdown events.
    """
    try:
        # Startup logic
        logger.info("==========================================")
        logger.info("Starting FastAPI application...")
        logger.info(f"Working directory: {os.getcwd()}")
        logger.info(f"Environment variables: PORT={os.environ.get('PORT', 'not set')}")
        logger.info(f"Database: POSTGRES_HOST={os.environ.get('POSTGRES_HOST', 'not set')}")
        yield
    except Exception as e:
        logger.error(f"Error during startup: {e}")
        raise
    finally:
        # Shutdown logic
        logger.info("Shutting down application...")
        logger.info("==========================================")

# Create FastAPI application instance
app = FastAPI(
    title=openapi_config.name,
    version=openapi_config.version,
    description=openapi_config.description,
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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

# Simple test endpoint to check environment variables
@app.get("/debug", tags=["Debug"])
async def debug_info():
    """Debug endpoint that returns environment information."""
    env_info = {
        "working_directory": os.getcwd(),
        "port": os.environ.get("PORT", "not set"),
        "postgres_host": os.environ.get("POSTGRES_HOST", "not set"),
        "postgres_port": os.environ.get("POSTGRES_PORT", "not set"),
        "postgres_user": os.environ.get("POSTGRES_USER", "not set"),
        "postgres_db": os.environ.get("POSTGRES_DB", "not set"),
    }
    logger.info(f"Debug endpoint accessed: {env_info}")
    return env_info

try:
    # Initialize the application
    logger.info("Starting application initialization...")
    init(app)
    logger.info("Application initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize application: {str(e)}")
    import traceback
    logger.error(traceback.format_exc())
    # Don't raise the exception, let the application start anyway
    # This allows the health endpoint to work even if database fails
    pass 