from fastapi import Depends
from sqlalchemy.sql.annotation import Annotated

from app.models.user import User, Salt
from app.routers.dto.JwtToken import JwtTokenResponse, JwtBearerTokenResponse
from app.routers.dto.user import NewUserRequest, UserResponse, SigninRequest
from app.setvices.service_base import ServiceBase
from passlib.context import CryptContext
import bcrypt
from app.config.database import db_session
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

SECRET_KEY = 'df50448df8c9430513b8196e4ac445345887f8fd95ff4adc0b2fe766aed1909a'
ALGORITHM = 'HS256'
REFRESH_TOKEN_EXPIRES_IN = timedelta(days=7)
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth")

class AuthService(ServiceBase):
    def __init__(self, db=None):
        super().__init__(db)
        self.bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def add(self, request: NewUserRequest, session: db_session = None) -> None | User:
        salt_str = bcrypt.gensalt().decode("utf-8")

        user = self._mapToNewUser(request, salt_str)

        _session = self._get_session(session)
        _session.add(user)
        _session.add(self._new_salt(user, salt_str))
        _session.commit()
        _session.refresh(user)

        return user

    def signin(self, request: SigninRequest, session: db_session = None) -> None | User:
        _session = self._get_session(session)
        user = _session.query(User).filter(User.email == request.email).first()
        if user is None:
            return None

        salt = _session.query(Salt).filter(Salt.user == user).first()
        if salt is None:
            return None

        salted_password = request.password + salt.salt
        if bcrypt.checkpw(salted_password.encode('utf-8'), user.hashed_password.encode('utf-8')):
            return user
        else:
            return None

    def authenticate(self, user_name: str, password: str, session: db_session = None) -> None | JwtBearerTokenResponse:
        _session = self._get_session(session)
        user = _session.query(User).filter(User.email == user_name).first()
        if user is None:
            return None

        salt = _session.query(Salt).filter(Salt.user == user).first()
        if salt is None:
            return None

        salted_password = password + salt.salt
        if bcrypt.checkpw(salted_password.encode('utf-8'), user.hashed_password.encode('utf-8')):
            access_token = self.create_access_token(user.email, user.public_id, timedelta(minutes=20))
            refresh_token = self.create_refresh_token(user.email, user.public_id)
            return JwtBearerTokenResponse(access_token, refresh_token)
        else:
            return None

    def create_access_token(self, user_name: str, user_id: str, expires_delta: timedelta) -> str:
        expires = datetime.now(timezone.utc) + expires_delta
        access_token = {
            'sub': user_name,
            'id': str(user_id),
            "exp": expires,
            "iat": datetime.now(timezone.utc),
            "type": "access_token"
        }

        return jwt.encode(access_token, SECRET_KEY, algorithm=ALGORITHM)

    def create_refresh_token(self, user_name: str, user_id: str) -> str:
        expires = datetime.now(timezone.utc) + REFRESH_TOKEN_EXPIRES_IN
        refresh_token = {
            'sub': user_name,
            'id': str(user_id),
            "exp": expires,
            "iat": datetime.now(timezone.utc),
            "type": "refresh_token"
        }

        return jwt.encode(refresh_token, SECRET_KEY, algorithm=ALGORITHM)

    def get_current_user(self, token: Annotated[str, Depends(oauth2_bearer)]) -> None | str:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            if payload["type"] == "access_token":
                user_name: str = payload["sub"]
                user_id: str = payload["id"]
                if user_name is None or user_id is None:
                    return None
                return user_name
            else:
                return None
        except JWTError:
            return None


    def _mapToNewUser(self, userRequest: NewUserRequest, salt: str) -> User:
        user = User()
        user.email = userRequest.email
        user.first_name = userRequest.first_name
        user.last_name = userRequest.last_name
        user.hashed_password = self.bcrypt_context.hash(userRequest.password + salt)
        user.role = userRequest.role
        user.is_active = True
        return user


    def _new_salt(self, user: User, salt_str: str) -> Salt:
        salt = Salt()
        salt.user = user
        salt.salt = salt_str
        return salt
