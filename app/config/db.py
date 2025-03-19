"""Database configuration module."""
from betterconf import Config, field
from betterconf.config import as_dict

DB_MODELS = ["app.core.models.tortoise"]
POSTGRES_DB_URL = "postgres://{postgres_user}:{postgres_password}@{postgres_host}:{postgres_port}/{postgres_db}"
SQLITE_DB_URL = "sqlite://db.sqlite3"

class PostgresSettings(Config):
    """Postgres environment settings."""
    postgres_user: str = field("POSTGRES_USER", default="postgres")
    postgres_password: str = field("POSTGRES_PASSWORD", default="postgres")
    postgres_db: str = field("POSTGRES_DB", default="mydb")
    postgres_port: str = field("POSTGRES_PORT", default="5432")
    postgres_host: str = field("POSTGRES_HOST", default="postgres")


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
        db_url = POSTGRES_DB_URL.format(**as_dict(postgres))
        del postgres
        modules = {"models": DB_MODELS}
        return TortoiseSettings(db_url=db_url, modules=modules, generate_schemas=True) 