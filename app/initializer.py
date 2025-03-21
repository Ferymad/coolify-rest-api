"""Application initialization module."""
from inspect import getmembers

from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from tortoise.exceptions import DoesNotExist, IntegrityError, DBConnectionError
from loguru import logger

from app.config import tortoise_config
from app.utils.api.router import TypedAPIRouter

def init(app: FastAPI) -> None:
    """
    Initialize application components.
    
    Args:
        app: The FastAPI application instance.
    """
    try:
        logger.info("Initializing exception handlers...")
        init_exceptions_handlers(app)
        
        logger.info("Initializing database...")
        init_db(app)
        
        logger.info("Initializing routers...")
        init_routers(app)
        
        logger.success("Application initialized successfully!")
    except Exception as e:
        logger.error(f"Failed to initialize application: {e}")
        raise

def init_exceptions_handlers(app: FastAPI) -> None:
    """
    Initialize application exception handlers.
    
    Args:
        app: The FastAPI application instance.
    """
    from app.core.exceptions.handlers import tortoise_exception_handler

    app.add_exception_handler(DoesNotExist, tortoise_exception_handler)
    app.add_exception_handler(IntegrityError, tortoise_exception_handler)
    app.add_exception_handler(DBConnectionError, tortoise_exception_handler)

def init_db(app: FastAPI) -> None:
    """
    Initialize database connection with Tortoise ORM.
    
    Args:
        app: The FastAPI application instance.
    """
    try:
        logger.info(f"Registering Tortoise ORM with URL: {tortoise_config.db_url.replace(tortoise_config.db_url.split('@')[0].split('://')[-1], '******')}")
        register_tortoise(
            app,
            db_url=tortoise_config.db_url,
            generate_schemas=tortoise_config.generate_schemas,
            modules=tortoise_config.modules,
        )
        logger.success("Database initialized successfully!")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise

def init_routers(app: FastAPI) -> None:
    """
    Initialize API routers from the routers module.
    
    Args:
        app: The FastAPI application instance.
    """
    from app.core import routers

    routers_list = [o[1] for o in getmembers(routers) if isinstance(o[1], TypedAPIRouter)]
    logger.info(f"Found {len(routers_list)} routers to register")
    
    for router in routers_list:
        logger.info(f"Registering router with prefix: {router.prefix}")
        app.include_router(**router.dict()) 