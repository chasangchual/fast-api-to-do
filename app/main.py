from fastapi import FastAPI

from app import routers
from app.routers.categories import categories_router
from app.routers.todos import todos_router
from app.setvices.service_container import ServiceContainer
from app.routers import categories, todos
app = FastAPI()

srvice_container = ServiceContainer()
srvice_container.wire(modules=[categories, todos])
app.include_router(categories_router)
app.include_router(todos_router)