from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import Optional
from ..database import get_db
from ..models import Video, Channel
from ..schemas import FeedResponse

router = APIRouter()

@router.get("", response_model=FeedResponse)
@router.get("/feed", response_model=FeedResponse)
async def get_feed(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=50),
    sort_by: str = Query("latest"),
    db: Session = Depends(get_db),
):
    query = db.query(Video).filter(Video.is_public == True, Video.moderation_status == 'approved')
    if sort_by == 'popular':
        query = query.order_by(desc(Video.view_count))
    elif sort_by == 'community':
        query = query.order_by(desc(Video.community_rating))
    else:
        query = query.order_by(desc(Video.published_at))

    total = query.count()
    videos = query.offset((page - 1) * page_size).limit(page_size).all()
    results = []
    for video in videos:
        channel = db.query(Channel).filter(Channel.id == video.channel_id).first()
        results.append({
            "id": video.id,
            "title": video.title,
            "description": video.description,
            "thumbnail_url": video.thumbnail_url,
            "video_url": video.video_url,
            "duration": video.duration,
            "view_count": video.view_count,
            "like_count": video.like_count,
            "comment_count": video.comment_count,
            "share_count": video.share_count,
            "community_rating": video.community_rating,
            "channel": {
                "id": channel.id if channel else 0,
                "name": channel.name if channel else "Unknown",
                "profile_picture_url": channel.profile_picture_url if channel else None,
                "subscriber_count": channel.subscriber_count if channel else 0,
            },
            "created_at": video.created_at,
            "published_at": video.published_at,
        })
    return {"results": results, "total": total, "page": page, "page_size": page_size, "next_page": page + 1 if (page * page_size) < total else None}

