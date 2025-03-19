"""Tortoise ORM models for the application."""
from tortoise import Model, fields
import uuid

class Item(Model):
    """Item model for storing product or service data."""
    id = fields.UUIDField(pk=True, default=uuid.uuid4)
    name = fields.CharField(max_length=255)
    price = fields.FloatField()
    description = fields.TextField(null=True)
    is_offer = fields.BooleanField(default=False)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    
    class Meta:
        """Model metadata."""
        table = "items"
    
    def __str__(self) -> str:
        """String representation of the model."""
        return f"Item {self.name} (ID: {self.id})"
