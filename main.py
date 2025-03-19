from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional, Dict
import uuid
import os

app = FastAPI(
    title="FastAPI REST API",
    description="A simple REST API built with FastAPI for deployment on Hetzner with Coolify",
    version="1.0.0"
)

# Simple in-memory database
items_db: Dict[str, dict] = {}

class Item(BaseModel):
    """Data model for an item in the store."""
    name: str
    price: float
    description: Optional[str] = None
    is_offer: Optional[bool] = None

class ItemResponse(Item):
    """Data model for item responses that includes the ID."""
    id: str

@app.get("/", tags=["Root"])
def read_root():
    """Root endpoint that returns a welcome message."""
    return {"message": "Welcome to the FastAPI REST API", "status": "online"}

@app.get("/items", response_model=List[ItemResponse], tags=["Items"])
def list_items():
    """List all items in the database."""
    return [{"id": item_id, **item} for item_id, item in items_db.items()]

@app.post("/items", response_model=ItemResponse, status_code=status.HTTP_201_CREATED, tags=["Items"])
def create_item(item: Item):
    """Create a new item and store it in the database."""
    item_id = str(uuid.uuid4())
    items_db[item_id] = item.model_dump()
    return {"id": item_id, **item.model_dump()}

@app.get("/items/{item_id}", response_model=ItemResponse, tags=["Items"])
def read_item(item_id: str):
    """Get a specific item by its ID."""
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"id": item_id, **items_db[item_id]}

@app.put("/items/{item_id}", response_model=ItemResponse, tags=["Items"])
def update_item(item_id: str, item: Item):
    """Update an existing item by its ID."""
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    items_db[item_id] = item.model_dump()
    return {"id": item_id, **item.model_dump()}

@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Items"])
def delete_item(item_id: str):
    """Delete an item by its ID."""
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    del items_db[item_id]
    return None

@app.get("/health", tags=["Health"])
def health_check():
    """Health check endpoint for monitoring."""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    # Get port from environment variable or use default
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port) 