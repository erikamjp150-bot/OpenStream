from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Playlist

router = APIRouter()

@router.get("/", response_model=list[dict])
async def list_playlists(db: Session = Depends(get_db)):
    playlists = db.query(Playlist).all()
    return [{"id": p.id, "name": p.name, "description": p.description} for p in playlists]
