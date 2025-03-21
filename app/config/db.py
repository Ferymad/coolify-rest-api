"""Database configuration module."""
import os
import sys
import socket
from loguru import logger

DB_MODELS = ["app.core.models.tortoise"]

# Simple fallback to SQLite if PostgreSQL connection fails
POSTGRES_DB_URL = "postgres://{postgres_user}:{postgres_password}@{postgres_host}:{postgres_port}/{postgres_db}"
SQLITE_DB_URL = "sqlite://db.sqlite3"

class PostgresSettings:
    """Postgres environment settings."""
    def __init__(self):
        # Explicitly read from environment
        self.postgres_user = os.environ.get("POSTGRES_USER", "postgres")
        self.postgres_password = os.environ.get("POSTGRES_PASSWORD", "postgres")
        self.postgres_db = os.environ.get("POSTGRES_DB", "mydb")
        self.postgres_port = os.environ.get("POSTGRES_PORT", "5432")
        
        # Try to determine the best postgres host
        self.postgres_host = self._determine_postgres_host()
        
        # Log the settings to help with debugging
        logger.info(f"PostgreSQL Settings loaded from environment")
        logger.info(f"Host: {self.postgres_host}")
        logger.info(f"Port: {self.postgres_port}")
        logger.info(f"Database: {self.postgres_db}")
        logger.info(f"User: {self.postgres_user}")
        logger.info(f"All ENV variables: {', '.join([f'{k}={v}' for k, v in os.environ.items() if 'POSTGRES' in k])}")
    
    def _determine_postgres_host(self):
        """Try different strategies to determine the best PostgreSQL host."""
        # Get the host from the environment variable
        host = os.environ.get("POSTGRES_HOST", "postgres")
        
        # If running in Coolify with the default value, try some alternate options
        if host == "postgres":
            # Check if host.docker.internal is reachable (works on Docker Desktop)
            if self._is_host_reachable("host.docker.internal"):
                logger.info("Using host.docker.internal as PostgreSQL host")
                return "host.docker.internal"
            
            # Check if postgres.coolify is reachable (might work in Coolify network)
            if self._is_host_reachable("postgres.coolify"):
                logger.info("Using postgres.coolify as PostgreSQL host")
                return "postgres.coolify"
        
        logger.info(f"Using {host} as PostgreSQL host")
        return host
    
    def _is_host_reachable(self, host):
        """Check if a host is reachable on the PostgreSQL port."""
        try:
            port = int(self.postgres_port)
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)
                result = s.connect_ex((host, port))
                reachable = (result == 0)
                logger.info(f"Host {host}:{port} reachable: {reachable}")
                return reachable
        except Exception as e:
            logger.warning(f"Error checking if {host} is reachable: {e}")
            return False


class TortoiseSettings:
    """Tortoise ORM configuration settings."""
    def __init__(self, db_url: str, modules: dict, generate_schemas: bool):
        self.db_url = db_url
        self.modules = modules
        self.generate_schemas = generate_schemas

    @classmethod
    def generate(cls) -> "TortoiseSettings":
        """Generate Tortoise ORM configuration from environment settings."""
        postgres = PostgresSettings()
        
        try:
            # Format the database URL with the settings
            db_url = POSTGRES_DB_URL.format(
                postgres_user=postgres.postgres_user,
                postgres_password=postgres.postgres_password,
                postgres_host=postgres.postgres_host,
                postgres_port=postgres.postgres_port,
                postgres_db=postgres.postgres_db
            )
            
            # Log the final URL (with password masked)
            masked_url = db_url.replace(postgres.postgres_password, "********")
            logger.info(f"Database URL: {masked_url}")
        except Exception as e:
            logger.error(f"Error creating PostgreSQL connection string: {e}")
            logger.warning("Falling back to SQLite database")
            db_url = SQLITE_DB_URL
        
        modules = {"models": DB_MODELS}
        return TortoiseSettings(db_url=db_url, modules=modules, generate_schemas=True) 