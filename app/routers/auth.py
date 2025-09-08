from fastapi import APIRouter
from starlette import status

from app.routers.dto.user import UserRequest, UserResponse
from app.config.database import db_session
from app.setvices.auth_service import AuthService
from app.setvices.service_container import ServiceContainer
from fastapi.params import Depends
from app.models.user import User
from dependency_injector.wiring import inject, Provide

auth_router = APIRouter(
    prefix="/auth"
)


@auth_router.post("/signup", status_code=status.HTTP_201_CREATED)
@inject
def signup(request: UserRequest, session: db_session,
           auth_service: AuthService = Depends(Provide[ServiceContainer.auth_service])) -> UserResponse:
    user = auth_service.add(request, session)
    return UserResponse(user)
