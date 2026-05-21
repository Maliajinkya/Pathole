from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from app.routes import router
from app.database import init_db
import os

# Init DB on startup
init_db()

app = FastAPI(
    title="Pothole Detection System",
    description="AI-powered pothole detection for Gram Panchayat",
    version="1.0.0"
)

# Allow requests from browser / mobile app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# Mount static files and templates
os.makedirs("static", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# Include API routes under /api prefix
app.include_router(router, prefix="/api")


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})


# Auto-generated API docs available at:
# http://localhost:8000/docs       ← Swagger UI
# http://localhost:8000/redoc      ← ReDoc