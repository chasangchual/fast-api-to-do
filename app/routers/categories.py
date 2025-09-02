from typing import Annotated, List
from uuid import UUID
from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from dependency_injector.wiring import inject, Provide
from starlette import status
from app.models.todo import Category
from app.config.database import db_dependency
from app.routers.dto.category import CategoryResponse, CategoryRequest
from app.setvices.catetory_service import CategoryService
from app.setvices.service_container import ServiceContainer

categories_router = APIRouter(
    prefix="/categories"
)


@categories_router.get("", status_code=status.HTTP_200_OK)
@inject
def get_all(session: db_dependency,
            category_service: CategoryService = Depends(Provide[ServiceContainer.category_service])) -> List[
    CategoryResponse]:
    categories = category_service.find_all(session)
    return [CategoryResponse(category) for category in categories]


@categories_router.get("/{public_id}", status_code=status.HTTP_200_OK)
@inject
def find_by_id(public_id: UUID, session: db_dependency,
               category_service: CategoryService = Depends(
                   Provide[ServiceContainer.category_service])) -> CategoryResponse:
    category = category_service.find_by_id(public_id, session)
    if category is None:
        raise HTTPException(status_code=404, detail=f"Category with id [{public_id}] not found")
    return CategoryResponse(category)


@categories_router.post("", status_code=status.HTTP_201_CREATED)
@inject
def create(category: CategoryRequest, session: db_dependency,
           category_service: CategoryService = Depends(Provide[ServiceContainer.category_service])) -> CategoryResponse:
    category_service.set_session(session)
    found = category_service.find_by_name(category.name)
    if found is not None:
        raise HTTPException(status_code=400, detail=f"Category with name [{category.name}] already exists")

    new_category = category_service.add(Category(category.name))
    return CategoryResponse(new_category)


@categories_router.put("/{public_id}", status_code=status.HTTP_201_CREATED)
@inject
def update(public_id: UUID, category: CategoryRequest, session: db_dependency,
           category_service: CategoryService = Depends(Provide[ServiceContainer.category_service])) -> CategoryResponse:
    category_service.set_session(session)
    to_be_updated = category_service.find_by_id(public_id)
    if to_be_updated is None:
        raise HTTPException(status_code=404, detail=f"Category with id [{public_id}] not found")

    find_by_name = category_service.find_by_name(category.name)
    if find_by_name is not None:
        raise HTTPException(status_code=400, detail=f"Category with name [{category.name}] already exists")

    to_be_updated.name = category.name
    to_be_updated = category_service.update(to_be_updated)
    return CategoryResponse(to_be_updated)


@categories_router.delete("/{public_id}", status_code=status.HTTP_200_OK)
@inject
def delete_by_id(public_id: UUID, session: db_dependency,
                 category_service: CategoryService = Depends(Provide[ServiceContainer.category_service])):
    category_service.set_session(session)
    category = category_service.find_by_id(public_id)
    if category is None:
        raise HTTPException(status_code=404, detail=f"Category with id [{public_id}] not found")
    category_service.delete(category)
