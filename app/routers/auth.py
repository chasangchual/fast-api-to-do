from fastapi import APIRouter, HTTPException
from starlette import status
from typing import Any, Annotated

from app.routers.dto.JwtToken import JwtTokenResponse, JwtBearerTokenResponse
from app.routers.dto.user import NewUserRequest, UserResponse, SigninRequest
from app.config.database import db_session
from app.setvices.auth_service import AuthService
from app.setvices.service_container import ServiceContainer
from app.routers.dto.JwtToken import DEFAULT_ACCESS_TOKEN_EXPIRES_IN_SECONDS, DEFAULT_REFRESH_TOKEN_EXPIRES_IN_DAYS
from fastapi.params import Depends
from app.models.user import User
from dependency_injector.wiring import inject, Provide
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

auth_router = APIRouter(
    prefix="/users"
)


@auth_router.post("/signup", status_code=status.HTTP_201_CREATED)
@inject
async def signup(request: NewUserRequest, session: db_session,
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
async def signin(request: SigninRequest, session: db_session,
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


@auth_router.post("/auth", status_code=status.HTTP_200_OK)
@inject
async def get_token(request_form: Annotated[OAuth2PasswordRequestForm, Depends()], session: db_session,
                    auth_service: AuthService = Depends(Provide[ServiceContainer.auth_service])) -> JwtTokenResponse:
    try:
        # verify client id and secret
        token = auth_service.authenticate(request_form.username, request_form.password,
                                          DEFAULT_ACCESS_TOKEN_EXPIRES_IN_SECONDS, DEFAULT_REFRESH_TOKEN_EXPIRES_IN_DAYS, session)
        if token is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid Signin Request")
        return token
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@auth_router.post("/access_token", status_code=status.HTTP_200_OK)
@inject
async def get_token(access_token: str,
                    session: db_session,
                    auth_service: AuthService = Depends(Provide[ServiceContainer.auth_service])) -> UserResponse:
    try:
        # verify client id and secret
        user = await auth_service.get_current_user(access_token, session)

        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid access token or expired access token.")
        return UserResponse(user)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
