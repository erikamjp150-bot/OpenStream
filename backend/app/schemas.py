from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime


class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    full_name: Optional[str] = None


class LoginRequest(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    full_name: Optional[str] = None


class ChannelResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    subscriber_count: int = 0


class VideoCreate(BaseModel):
    title: str
    description: Optional[str] = None
    category: Optional[str] = None
    tags: Optional[List[str]] = None
    is_public: bool = True


class VideoResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    video_url: str
    thumbnail_url: Optional[str] = None
    duration: Optional[float] = None
    category: Optional[str] = None
    tags: Optional[List[str]] = None
    view_count: int = 0
    like_count: int = 0
    comment_count: int = 0
    community_rating: float = 0.0
    moderation_status: str = "pending"
    channel: Optional[ChannelResponse] = None
    created_at: datetime


class FeedResponse(BaseModel):
    results: List[VideoResponse]
    total: int
    page: int
    page_size: int
    next_page: Optional[int] = None


class CommentCreate(BaseModel):
    content: str = Field(min_length=1, max_length=500)


class CommentResponse(BaseModel):
    id: int
    content: str
    author_id: int
    video_id: int
    like_count: int = 0
    created_at: datetime
