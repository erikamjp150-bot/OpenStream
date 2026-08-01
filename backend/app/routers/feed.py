from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc, func, or_
from typing import Optional, List
from ..database import get_db
from ..models import Video, Channel, Subscription, User
from ..schemas import VideoResponse, FeedResponse
from ..config import settings
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/feed", response_model=FeedResponse)
async def get_feed(
    user_id: Optional[int] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=50),
    sort_by: str = Query("relevance", regex="^(relevance|latest|popular|community)$"),
    db: Session = Depends(get_db)
):
    """
    Get personalized video feed with user-controlled ranking.
    Options: relevance (default), latest, popular, community-rated.
    """
    # Base query: only public videos
    query = db.query(Video).filter(Video.is_public == True, Video.moderation_status == 'approved')
    
    # Get subscribed channels if user is logged in
    subscribed_channel_ids = []
    if user_id:
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            subscriptions = db.query(Subscription.channel_id).filter(Subscription.subscriber_id == user_id).all()
            subscribed_channel_ids = [s[0] for s in subscriptions]
    
    # Apply sorting based on user preference
    if sort_by == "latest":
        query = query.order_by(desc(Video.published_at))
    elif sort_by == "popular":
        query = query.order_by(desc(Video.view_count))
    elif sort_by == "community":
        query = query.order_by(desc(Video.community_rating))
    else:  # relevance (default) - prioritizes subscriptions + recency
        if subscribed_channel_ids:
            # Prioritize subscribed channels, then recency
            query = query.order_by(
                Video.channel_id.in_(subscribed_channel_ids).desc(),
                desc(Video.published_at)
            )
        else:
            query = query.order_by(desc(Video.published_at))
    
    # Pagination
    total = query.count()
    videos = query.offset((page - 1) * page_size).limit(page_size).all()
    
    # Format response
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
                "id": channel.id,
                "name": channel.name,
                "profile_picture_url": channel.profile_picture_url,
                "subscriber_count": channel.subscriber_count
            },
            "created_at": video.created_at.isoformat(),
            "published_at": video.published_at.isoformat() if video.published_at else None
        })
    
    return {
        "results": results,
        "total": total,
        "page": page,
        "page_size": page_size,
        "next_page": page + 1 if (page * page_size) < total else None
    }
