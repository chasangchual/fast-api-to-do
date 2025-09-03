from fastapi import FastAPI

from app import routers
from app.routers import auth, categories, todos
from app.setvices.service_container import ServiceContainer
from app.routers import categories, todos
app = FastAPI()

srvice_container = ServiceContainer()
srvice_container.wire(modules=[categories, todos])
app.include_router(auth.auto_router)
app.include_router(categories.categories_router)
app.include_router(todos.todos_router)
