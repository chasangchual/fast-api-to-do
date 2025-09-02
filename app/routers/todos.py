from fastapi import APIRouter, HTTPException
from app.config.database import db_dependency
from app.routers.dto.todo import TodoResponse, TodoRequest
from starlette import status
from app.setvices.todo_service import TodoService
from app.setvices.catetory_service import CategoryService
from app.setvices.service_container import ServiceContainer
from fastapi.params import Depends
from dependency_injector.wiring import inject, Provide
from app.models.todo import ToDo
from uuid import UUID

todos_router = APIRouter(
    prefix="/todos"
)


@todos_router.get("", status_code=200)
@inject
def get_all(session: db_dependency,
            todo_service: TodoService = Depends(Provide[ServiceContainer.todo_service])):
    todos = todo_service.find_all(session)
    return [TodoResponse(todo) for todo in todos]


@todos_router.get("/{public_id}", status_code=200)
@inject
def find_by_id(public_id: UUID, session: db_dependency,
               todo_service: TodoService = Depends(Provide[ServiceContainer.todo_service])):
    todo = todo_service.find_by_id(public_id, session)
    if todo is None:
        raise HTTPException(status_code=404, detail=f"Todo with id [{public_id}] not found")

    return TodoResponse(todo)


@todos_router.post("", status_code=status.HTTP_201_CREATED)
@inject
def create_todo(request: TodoRequest, session: db_dependency,
                todo_service: TodoService = Depends(Provide[ServiceContainer.todo_service]),
                category_service: CategoryService = Depends(
                    Provide[ServiceContainer.category_service])) -> TodoResponse:
    category = category_service.find_by_id(request.category_public_id, session)
    if category is None:
        raise HTTPException(status_code=404, detail=f"Category with id [{request.category_public_id}] not found")

    todo = todo_service.add(ToDo(category, request.title, request.description, request.priority, request.is_completed),
                            session)
    if todo is None:
        raise HTTPException(status_code=500, detail=f"Failed to add a new ToDo")

    return TodoResponse(todo)

@categories_router.delete("/{public_id}", status_code=status.HTTP_200_OK)
@inject
def delete_by_id(public_id: UUID, session: db_dependency,
                 todo_service: TodoService = Depends(Provide[ServiceContainer.todo_service])):
    todo_service.set_session(session)
    category = todo_service.find_by_id(public_id)
    if category is None:
        raise HTTPException(status_code=404, detail=f"ToDo with id [{public_id}] not found")
    todo_service.delete(category)
