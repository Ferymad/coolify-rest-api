"""OpenAPI configuration module."""
from betterconf import Config, field

class OpenAPISettings(Config):
    """OpenAPI settings from environment variables."""
    name: str = field("APP_NAME", default="FastAPI REST API")
    version: str = field("APP_VERSION", default="1.0.0")
    description: str = field(
        "APP_DESCRIPTION",
        default="A RESTful API built with FastAPI and Tortoise ORM for deployment on Hetzner with Coolify"
    ) 