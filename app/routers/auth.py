from fastapi import APIRouter
from starlette import status
from dependency_injector.wiring import inject, Provide

auto_router = APIRouter(
    prefix="/auth"
)

@auto_router.get("/login", status_code=status.HTTP_200_OK)
@inject
async def login():
    return {"message": "Login"}