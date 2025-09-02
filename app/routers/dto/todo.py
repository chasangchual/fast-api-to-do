from pydantic import BaseModel, Field
from uuid import UUID

from app.models.todo import ToDo

class TodoResponse(BaseModel):
    public_id: UUID
    category_public_id: UUID
    title: str
    description: str
    priority: int
    is_completed: bool

    model_config = {
        "json_schema_extra": {
            "example": {
                "public_id": "e77b0399-5306-4b7b-9cc2-9ca89211585b",
                "category_public_id": "17788c27-4b20-4245-9cfa-caed852eca7b",
                "title": "Process monthly order request",
                "description": "complete in the first week of the month",
                "priority": 3,
                "is_completed": False,
            }
        }
    }

    def __init__(self, todo: ToDo):
        todo_data = {
            "public_id": todo.public_id,
            "category_public_id": todo.category.public_id,
            "title": todo.title,
            "description": todo.description,
            "priority": todo.priority,
            "is_completed": todo.is_completed,
        }
        super().__init__(**todo_data)


class TodoRequest(BaseModel):
    category_public_id: UUID
    title: str = Field(..., min_length=3, max_length=50)
    description: str  = Field(..., min_length=0, max_length=250)
    priority: int = Field(..., ge=1, le=5)
    is_completed: bool

    model_config = {
        "json_schema_extra": {
            "example": {
                "category_public_id": "17788c27-4b20-4245-9cfa-caed852eca7b",
                "title": "Process monthly order request",
                "description": "complete in the first week of the month",
                "priority": 3,
                "is_completed": False,
            }
        }
    }
