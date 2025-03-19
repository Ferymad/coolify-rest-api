"""Router exports for the application."""
from app.utils.api.router import TypedAPIRouter
from .items import router as items_router

items = TypedAPIRouter(router=items_router, prefix="/items", tags=["Items"])
