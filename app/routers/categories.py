from typing import Annotated, List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status
from app.models.todo import Category
from app.config.database import db_dependency
from app.routers.dto.todo import CategoryResponse

categories_router = APIRouter(
    prefix="/categories"
)

@categories_router.get("/", status_code=status.HTTP_200_OK)
def get_all_categories(db: db_dependency) -> List[CategoryResponse]:
    categories = db.query(Category).all()
    return [CategoryResponse(category) for category in categories]

