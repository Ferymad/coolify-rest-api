"""Router for Item CRUD operations."""
from fastapi import APIRouter, HTTPException, status
from typing import List
import uuid

from app.core.models.tortoise import Item as ItemModel
from app.core.models.pydantic import Item, ItemCreate, ItemUpdate, ItemInDB

router = APIRouter()

@router.post("/", response_model=Item, status_code=status.HTTP_201_CREATED, description="Create a new item")
async def create_item(item: ItemCreate):
    """Create a new item in the database."""
    item_obj = await ItemModel.create(
        id=uuid.uuid4(),
        name=item.name,
        price=item.price,
        description=item.description,
        is_offer=item.is_offer
    )
    return await Item.from_tortoise_orm(item_obj)

@router.get("/", response_model=List[Item], description="Get all items")
async def get_items():
    """Get all items from the database."""
    return await Item.from_queryset(ItemModel.all())

@router.get("/{item_id}", response_model=Item, description="Get an item by ID")
async def get_item(item_id: uuid.UUID):
    """Get a specific item by its ID."""
    item = await ItemModel.filter(id=item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return await Item.from_tortoise_orm(item)

@router.put("/{item_id}", response_model=Item, description="Update an item")
async def update_item(item_id: uuid.UUID, item_data: ItemUpdate):
    """Update an existing item by its ID."""
    item = await ItemModel.filter(id=item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    # Update only the fields that are provided
    update_data = item_data.dict(exclude_unset=True)
    if update_data:
        for field, value in update_data.items():
            setattr(item, field, value)
        await item.save()
    
    return await Item.from_tortoise_orm(item)

@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT, description="Delete an item")
async def delete_item(item_id: uuid.UUID):
    """Delete an item by its ID."""
    deleted_count = await ItemModel.filter(id=item_id).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail="Item not found")
    return None 