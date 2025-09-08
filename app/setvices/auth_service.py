from app.models.user import User, Salt
from app.routers.dto.user import UserRequest, UserResponse
from app.setvices.service_base import ServiceBase
from passlib.context import CryptContext
import bcrypt
from app.config.database import db_session


class AuthService(ServiceBase):
    def __init__(self, db=None):
        super().__init__(db)
        self.bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def add(self, request: UserRequest, session: db_session = None) -> None | User:
        salt_str = bcrypt.gensalt().decode("utf-8")

        user = self._mapToNewUser(request, salt_str)

        _session = self._get_session(session)
        _session.add(user)
        _session.add(self._new_salt(user, salt_str))
        _session.commit()
        _session.refresh(user)

        return user

    def _mapToNewUser(self, userRequest: UserRequest, salt: str) -> User:
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