from fastapi import FastAPI

from app.routers.categories import categories_router

app = FastAPI()

app.include_router(categories_router)