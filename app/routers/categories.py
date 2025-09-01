from typing import Annotated, List
from uuid import UUID

from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from app.models.todo import Category
from app.config.database import db_dependency
from app.routers.dto.todo import CategoryResponse

categories_router = APIRouter(
    prefix="/categories"
)

@categories_router.get("", status_code=status.HTTP_200_OK)
def get_all_categories(db: db_dependency) -> List[CategoryResponse]:
    categories = db.query(Category).all()
    return [CategoryResponse(category) for category in categories]

@categories_router.get("/{public_id}", status_code=status.HTTP_200_OK)
def get_category_by_id(public_id: UUID, db: db_dependency) -> CategoryResponse:
    category = db.query(Category).filter(Category.public_id == public_id).first()
    if category is not None:
        return CategoryResponse(category)
    raise HTTPException(status_code=404, detail=f"Category with id [{public_id}] not found")
