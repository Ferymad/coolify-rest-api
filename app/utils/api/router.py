"""Router utilities for FastAPI."""
from typing import List
from fastapi import APIRouter
from pydantic import BaseModel

class TypedAPIRouter(BaseModel):
    """Router with additional metadata for easier management."""
    router: APIRouter
    prefix: str = ""
    tags: List[str] = []
    
    def dict(self) -> dict:
        """Convert to dict for FastAPI's include_router method."""
        return {
            "router": self.router,
            "prefix": self.prefix,
            "tags": self.tags
        } 