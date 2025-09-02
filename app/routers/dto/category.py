import uuid
from pydantic import BaseModel, Field
from uuid import UUID

from app.models.todo import Category


class CategoryResponse(BaseModel):
    public_id: UUID
    name: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "public_id": "e77b0399-5306-4b7b-9cc2-9ca89211585b",
                "name": "Work"
            }
        }
    }

    def __init__(self, category: Category):
        category_data = {
            "public_id": category.public_id,
            "name": category.name
        }
        super().__init__(**category_data)


class CategoryRequest(BaseModel):
    name: str = Field(..., min_length=3, max_length=50)

    def toCategory(self):
        return Category(self.name, uuid.uuid4())