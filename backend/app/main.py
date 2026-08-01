from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import auth, videos, channels, playlists, subscriptions, feed, admin
from .database import engine
from . import models
from .config import settings
import logging

# Create tables
models.Base.metadata.create_all(bind=engine)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="OpenStream API",
    description="An open-source, transparent alternative to YouTube",
    version="0.1.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["authentication"])
app.include_router(videos.router, prefix="/videos", tags=["videos"])
app.include_router(channels.router, prefix="/channels", tags=["channels"])
app.include_router(playlists.router, prefix="/playlists", tags=["playlists"])
app.include_router(subscriptions.router, prefix="/subscriptions", tags=["subscriptions"])
app.include_router(feed.router, prefix="/feed", tags=["feed"])
app.include_router(admin.router, prefix="/admin", tags=["administration"])

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "openstream-backend"}
