from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.config.database import db_session
from app.models import User
from app.setvices.auth_service import decode_token, AuthService
from fastapi.params import Depends
from fastapi import HTTPException, Request, status
from app.setvices.service_container import ServiceContainer
from dependency_injector.wiring import inject, Provide

security = HTTPBearer()


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    @inject
    async def __call__(self, request: Request, session: db_session,
                       auth_service: AuthService = Depends(Provide[ServiceContainer.auth_service])) -> User:
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if not credentials:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="Invalid authentication credentials.")

        if not credentials.scheme == 'Bearer':
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="Invalid authentication scheme, Bearer required.")
        jwt_properties = self.decode_token(credentials.credentials)
        if not jwt_properties:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="Invalid or expired token.")

        authenticated_user: User = auth_service.find_user_by_user_name(jwt_properties["sub"], session)

        if authenticated_user is None:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="Invalid or expired token.")
        return authenticated_user

    def decode_token(self, jwtToken: str) -> dict | None:
        try:
            payload = decode_token(jwtToken)
        except:
            payload = None

        return payload
