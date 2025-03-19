"""Pydantic models for request validation and response serialization."""
from pydantic import BaseModel, Field
from typing import Optional, List
from uuid import UUID
from tortoise.contrib.pydantic import pydantic_model_creator
from app.core.models.tortoise import Item as ItemModel

class ItemBase(BaseModel):
    """Base schema for Item data."""
    name: str
    price: float
    description: Optional[str] = None
    is_offer: Optional[bool] = None

class ItemCreate(ItemBase):
    """Schema for creating a new item."""
    pass

class ItemUpdate(BaseModel):
    """Schema for updating an existing item, all fields optional."""
    name: Optional[str] = None
    price: Optional[float] = None
    description: Optional[str] = None
    is_offer: Optional[bool] = None

# Generate Pydantic models from Tortoise models
Item = pydantic_model_creator(
    ItemModel, 
    name="Item",
    exclude=("created_at", "updated_at")
)

ItemInDB = pydantic_model_creator(
    ItemModel,
    name="ItemInDB",
)
