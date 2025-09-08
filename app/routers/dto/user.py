from pydantic import BaseModel, Field
from uuid import UUID
from app.models.user import User
class UserResponse(BaseModel):
    public_id: UUID
    email: str
    first_name: str
    last_name: str
    role: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "public_id": "e77b0399-5306-4b7b-9cc2-9ca89211585b",
                "email": "john.dow@not-gmail.com",
                "first_name": "John",
                "last_name": "Doe",
                "role": "USER"
            }
        }
    }

    def __init__(self, user: User):
        user_data = {
            "public_id": user.public_id,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "role": user.role
        }
        super().__init__(**user_data)

class UserRequest(BaseModel):
    email: str = Field(..., min_length=5, max_length=128)
    first_name: str = Field(..., min_length=1, max_length=64)
    last_name: str = Field(..., min_length=1, max_length=64)
    password: str = Field(..., min_length=5, max_length=64)
    role: str = Field(..., min_length=1, max_length=16)

    model_config = {
        "json_schema_extra": {
            "example": {
                "email": "john.dow@not-gmail.com",
                "first_name": "John",
                "last_name": "Doe",
                "password": "8d#kd#a23",
                "role": "USER"
            }
        }
    }