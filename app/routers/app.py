from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi import Request
from fastapi.templating import Jinja2Templates
from pathlib import Path

# BASE_DIR = Path(__file__).resolve().parent  # directory of this file
# TEMPLATES_DIR = BASE_DIR.parent / "templates"
#
# templates = Jinja2Templates(directory=TEMPLATES_DIR)
templates = Jinja2Templates(directory="templates")

app_router = APIRouter(
    prefix="/app"
)

@app_router.get("/home", status_code=200)
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})
