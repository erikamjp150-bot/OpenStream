from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Video

router = APIRouter()


@router.get("/moderation")
async def moderation_queue(db: Session = Depends(get_db)):
    videos = db.query(Video).filter(Video.moderation_status != "approved").all()
    return [{"id": v.id, "title": v.title, "status": v.moderation_status, "description": v.description} for v in videos]


@router.post("/moderation/{video_id}/review")
async def review_video(video_id: int, decision: str, db: Session = Depends(get_db)):
    video = db.query(Video).filter(Video.id == video_id).first()
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    video.moderation_status = "approved" if decision == "approve" else "rejected"
    db.commit()
    return {"ok": True, "status": video.moderation_status}
