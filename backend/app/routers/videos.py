from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, BackgroundTasks
from sqlalchemy.orm import Session
from datetime import datetime
from ..database import get_db
from ..models import Video, Channel
from ..schemas import VideoResponse
from ..services.video_processor import VideoProcessor
from ..services.storage import StorageService
from ..services.moderation import ContentModerator
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

video_processor = VideoProcessor()
storage = StorageService()
moderator = ContentModerator()

@router.post("/upload", response_model=VideoResponse)
async def upload_video(
    title: str = Form(...),
    description: str = Form(None),
    category: str = Form(None),
    tags: str = Form(None),
    is_public: bool = Form(True),
    video_file: UploadFile = File(...),
    background_tasks: BackgroundTasks = None,
    db: Session = Depends(get_db),
):
    channel = db.query(Channel).filter(Channel.id == 1).first()
    if not channel:
        raise HTTPException(status_code=400, detail="Default channel not found")
    if not video_file.content_type or not video_file.content_type.startswith('video/'):
        raise HTTPException(status_code=400, detail="File must be a video")

    temp_path = f"/tmp/{video_file.filename}"
    with open(temp_path, "wb") as f:
        content = await video_file.read()
        f.write(content)

    try:
        processed = video_processor.process_video(temp_path)
    except Exception as e:
        logger.error(f"Video processing failed: {e}")
        raise HTTPException(status_code=500, detail="Video processing failed")

    video_url = storage.upload_file(processed['output_path'], f"videos/1/{processed['video_id']}.mp4", content_type="video/mp4")
    thumbnail_url = storage.upload_file(processed['thumbnail_path'], f"thumbnails/1/{processed['video_id']}.jpg", content_type="image/jpeg")

    new_video = Video(
        channel_id=channel.id,
        title=title,
        description=description,
        video_url=video_url,
        thumbnail_url=thumbnail_url,
        duration=processed['metadata']['duration'],
        width=processed['metadata']['width'],
        height=processed['metadata']['height'],
        file_size=processed['metadata']['file_size'],
        category=category,
        tags=tags.split(',') if tags else [],
        is_public=is_public,
        published_at=datetime.utcnow()
    )

    db.add(new_video)
    db.commit()
    db.refresh(new_video)

    if background_tasks is not None:
        background_tasks.add_task(moderator.moderate_video, new_video.id, video_url, thumbnail_url)

    return new_video


@router.get("/{video_id}", response_model=VideoResponse)
async def get_video(video_id: int, db: Session = Depends(get_db)):
    video = db.query(Video).filter(Video.id == video_id).first()
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    return video
