from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Video

router = APIRouter()

@router.get("/moderation")
async def moderation_queue(db: Session = Depends(get_db)):
    videos = db.query(Video).filter(Video.moderation_status != "approved").all()
    return [{"id": v.id, "title": v.title, "status": v.moderation_status} for v in videos]
