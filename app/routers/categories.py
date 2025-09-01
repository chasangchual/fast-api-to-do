from typing import Annotated, List
from uuid import UUID

from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from app.models.todo import Category
from app.config.database import db_dependency
from app.routers.dto.todo import CategoryResponse, CategoryRequest

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
    if category is None:
        raise HTTPException(status_code=404, detail=f"Category with id [{public_id}] not found")
    return CategoryResponse(category)

@categories_router.post("", status_code=status.HTTP_201_CREATED)
def create_category(category: CategoryRequest, db: db_dependency) -> CategoryResponse:
    found = db.query(Category).filter(Category.name == category.name).first()
    if found is not None:
        raise HTTPException(status_code=400, detail=f"Category with name [{category.name}] already exists")

    db_category = Category(category.name)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return CategoryResponse(db_category)

@categories_router.put("/{public_id}", status_code=status.HTTP_201_CREATED)
def create_category(public_id: UUID, category: CategoryRequest, db: db_dependency) -> CategoryResponse:
    to_be_updated = db.query(Category).filter(Category.public_id == public_id).first()
    if to_be_updated is None:
        raise HTTPException(status_code=404, detail=f"Category with id [{public_id}] not found")

    to_be_updated = db.query(Category).filter(Category.name == category.name).first()
    if to_be_updated is not None:
        raise HTTPException(status_code=400, detail=f"Category with name [{category.name}] already exists")

    to_be_updated.name = category.name
    db.add(to_be_updated)
    db.commit()
    db.refresh(to_be_updated)
    return CategoryResponse(to_be_updated)

