"""Exception handlers for the application."""
from fastapi import Request
from fastapi.responses import JSONResponse
from tortoise.exceptions import DoesNotExist, IntegrityError, DBConnectionError
from loguru import logger

async def tortoise_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle Tortoise ORM exceptions with appropriate HTTP responses."""
    if isinstance(exc, DoesNotExist):
        logger.warning(f"Resource not found: {exc}")
        return JSONResponse(status_code=404, content={"detail": "Resource not found"})
    
    if isinstance(exc, IntegrityError):
        logger.error(f"Database integrity error: {exc}")
        return JSONResponse(status_code=400, content={"detail": "Database integrity constraint violated"})
    
    if isinstance(exc, DBConnectionError):
        logger.error(f"Database connection error: {exc}")
        return JSONResponse(status_code=503, content={"detail": "Database connection error"})
    
    # Handle generic database errors
    logger.error(f"Database error: {exc}")
    return JSONResponse(status_code=500, content={"detail": "Database error occurred"}) 