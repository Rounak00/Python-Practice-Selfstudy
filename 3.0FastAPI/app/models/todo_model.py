from beanie import Document
from pydantic import Field
from datetime import datetime
from typing import Optional

class Todo(Document):
    title: str = Field(..., max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    is_completed: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "todos"  # MongoDB collection name

    class Config:
        schema_extra = {
            "example": {
                "title": "Buy groceries",
                "description": "Milk, Bread, Eggs, Fruits",
                "is_completed": False
            }
        }
