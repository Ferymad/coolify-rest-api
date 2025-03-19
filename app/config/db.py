"""Database configuration module."""
import os
from loguru import logger

DB_MODELS = ["app.core.models.tortoise"]
POSTGRES_DB_URL = "postgres://{postgres_user}:{postgres_password}@{postgres_host}:{postgres_port}/{postgres_db}"
SQLITE_DB_URL = "sqlite://db.sqlite3"

class PostgresSettings:
    """Postgres environment settings."""
    def __init__(self):
        self.postgres_user = os.getenv("POSTGRES_USER", "postgres")
        self.postgres_password = os.getenv("POSTGRES_PASSWORD", "postgres")
        self.postgres_db = os.getenv("POSTGRES_DB", "mydb")
        self.postgres_port = os.getenv("POSTGRES_PORT", "5432")
        self.postgres_host = os.getenv("POSTGRES_HOST", "postgres")
        
        # Log the settings to help with debugging
        logger.info(f"PostgreSQL Settings: Host={self.postgres_host}, Port={self.postgres_port}, DB={self.postgres_db}")


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
        
        modules = {"models": DB_MODELS}
        return TortoiseSettings(db_url=db_url, modules=modules, generate_schemas=True) 