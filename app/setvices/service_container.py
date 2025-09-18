from dependency_injector import containers, providers

from app.config.database import db_session
from app.setvices.auth_service import AuthService
from app.setvices.catetory_service import CategoryService
from app.setvices.todo_service import TodoService

class ServiceContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    category_service = providers.Factory(CategoryService, session=db_session)
    todo_service = providers.Factory(TodoService, session=db_session)
    auth_service = providers.Factory(AuthService, session=db_session)