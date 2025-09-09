from fastapi import APIRouter, HTTPException
from starlette import status
from typing import Any

from app.routers.dto.user import NewUserRequest, UserResponse, SigninRequest
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
def signup(request: NewUserRequest, session: db_session,
           auth_service: AuthService = Depends(Provide[ServiceContainer.auth_service])) -> UserResponse:
    try:
        user = auth_service.add(request, session)
        return UserResponse(user)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@auth_router.post("/signin", status_code=status.HTTP_200_OK)
@inject
def signin(request: SigninRequest, session: db_session,
           auth_service: AuthService = Depends(Provide[ServiceContainer.auth_service])) -> UserResponse:
    try:
        user = auth_service.signin(request, session)
        if user is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid Signin Request")
        return UserResponse(user)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
