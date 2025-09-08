from fastapi import FastAPI

from app import models
from app import routers
from app.setvices.service_container import ServiceContainer
from app.routers import auth, categories, todos
app = FastAPI()

srvice_container = ServiceContainer()
srvice_container.wire(modules=[categories, todos, auth])
app.include_router(auth.auth_router)
app.include_router(categories.categories_router)
app.include_router(todos.todos_router)
