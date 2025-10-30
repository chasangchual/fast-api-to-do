from fastapi import FastAPI

from app.setvices.service_container import ServiceContainer
from app.routers import auth, categories, todos, app
from starlette.staticfiles import StaticFiles

todo_app = FastAPI()

todo_app.mount("/static", StaticFiles(directory="static"), name="static")
srvice_container = ServiceContainer()
srvice_container.wire(modules=[categories, todos, auth])
todo_app.include_router(auth.auth_router)
todo_app.include_router(categories.categories_router)
todo_app.include_router(todos.todos_router)
todo_app.include_router(app.app_router)
