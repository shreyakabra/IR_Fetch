from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import os
from dotenv import load_dotenv

load_dotenv()
from fastapi.middleware.cors import CORSMiddleware
import logging
from .models import DownloadRequest, DownloadResponse, ApiSettings
from .pipeline import run_pipeline
from .settings import load_settings_status, update_settings_env, SETTING_KEYS

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI(title="IR Downloader", version="0.1.0")

@app.middleware("http")
async def log_requests(request, call_next):
    logger.info(f"Incoming request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Response status: {response.status_code}")
    return response



# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/health")
def health():
    return {"ok": True}

@app.post("/download", response_model=DownloadResponse)
async def download(req: DownloadRequest):
    return await run_pipeline(req)

@app.post("/search", response_model=DownloadResponse)
async def search(req: DownloadRequest):
    """Alias for /download to support older frontend versions or caching issues."""
    return await run_pipeline(req)

# handy: list recent files
from .database import get_recent_files, init_database

# Initialize database on startup
init_database()

@app.get("/files")
def files():
    """Get recent files from database."""
    items = get_recent_files(limit=100)
    return {"items": items}

@app.get("/settings")
def get_settings():
    return load_settings_status()

@app.post("/settings")
def update_settings(body: ApiSettings):
    incoming = body.model_dump(exclude_none=True)
    if not incoming:
        return {"updated": []}
    update_settings_env(incoming)
    return {"updated": list(incoming.keys())}

# Serve React frontend static files (built with Vite)
if os.getenv("SERVE_STATIC", "false").lower() == "true":
    from fastapi.staticfiles import StaticFiles

    frontend_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "frontend", "dist")
    )

    if not os.path.exists(frontend_path):
        os.makedirs(frontend_path, exist_ok=True)

    app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")

