"""Application configuration module exports."""
from .db import TortoiseSettings
from .openapi import OpenAPISettings

tortoise_config = TortoiseSettings.generate()
openapi_config = OpenAPISettings()
