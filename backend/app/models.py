from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, Float, ForeignKey, JSON, BigInteger, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import pytz

Base = declarative_base()

def utc_now():
    return datetime.now(pytz.UTC)

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(100))
    bio = Column(Text)
    profile_picture_url = Column(String(500))
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), default=utc_now)
    updated_at = Column(DateTime(timezone=True), default=utc_now, onupdate=utc_now)
    
    # Relationships
    channel = relationship("Channel", back_populates="user", uselist=False)
    comments = relationship("Comment", back_populates="author")
    subscriptions = relationship("Subscription", foreign_keys="Subscription.subscriber_id", back_populates="subscriber")
    
class Channel(Base):
    __tablename__ = "channels"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    name = Column(String(100), unique=True, index=True, nullable=False)
    description = Column(Text)
    profile_picture_url = Column(String(500))
    banner_url = Column(String(500))
    subscriber_count = Column(Integer, default=0)
    total_view_count = Column(BigInteger, default=0)
    created_at = Column(DateTime(timezone=True), default=utc_now)
    updated_at = Column(DateTime(timezone=True), default=utc_now, onupdate=utc_now)
    
    # Relationships
    user = relationship("User", back_populates="channel")
    videos = relationship("Video", back_populates="channel")
    subscriptions = relationship("Subscription", foreign_keys="Subscription.channel_id", back_populates="channel")

class Video(Base):
    __tablename__ = "videos"
    
    id = Column(Integer, primary_key=True, index=True)
    channel_id = Column(Integer, ForeignKey("channels.id"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    video_url = Column(String(500), nullable=False)
    thumbnail_url = Column(String(500))
    duration = Column(Integer)  # Duration in seconds
    width = Column(Integer)
    height = Column(Integer)
    file_size = Column(BigInteger)
    
    # Engagement metrics
    view_count = Column(Integer, default=0)
    like_count = Column(Integer, default=0)
    comment_count = Column(Integer, default=0)
    share_count = Column(Integer, default=0)
    
    # Content metadata
    category = Column(String(50))
    tags = Column(JSON)  # List of tags
    is_public = Column(Boolean, default=True)
    is_members_only = Column(Boolean, default=False)
    community_rating = Column(Float, default=0.0)  # 0-1, user-voted quality
    
    # Moderation
    moderation_status = Column(String(20), default='pending')  # pending, approved, rejected
    wellness_score = Column(Float, default=0.5)
    
    created_at = Column(DateTime(timezone=True), default=utc_now)
    updated_at = Column(DateTime(timezone=True), default=utc_now, onupdate=utc_now)
    published_at = Column(DateTime(timezone=True))
    is_active = Column(Boolean, default=True)
    is_featured = Column(Boolean, default=False)
    
    # Relationships
    channel = relationship("Channel", back_populates="videos")
    comments = relationship("Comment", back_populates="video")
    playlist_videos = relationship("PlaylistVideo", back_populates="video")

class Comment(Base):
    __tablename__ = "comments"
    
    id = Column(Integer, primary_key=True, index=True)
    video_id = Column(Integer, ForeignKey("videos.id"), nullable=False)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    content = Column(Text, nullable=False)
    like_count = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), default=utc_now)
    updated_at = Column(DateTime(timezone=True), default=utc_now, onupdate=utc_now)
    is_deleted = Column(Boolean, default=False)
    
    # Relationships
    video = relationship("Video", back_populates="comments")
    author = relationship("User", back_populates="comments")

class Playlist(Base):
    __tablename__ = "playlists"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    is_public = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=utc_now)
    updated_at = Column(DateTime(timezone=True), default=utc_now, onupdate=utc_now)
    
    # Relationships
    user = relationship("User")
    playlist_videos = relationship("PlaylistVideo", back_populates="playlist")

class PlaylistVideo(Base):
    __tablename__ = "playlist_videos"
    
    id = Column(Integer, primary_key=True, index=True)
    playlist_id = Column(Integer, ForeignKey("playlists.id"), nullable=False)
    video_id = Column(Integer, ForeignKey("videos.id"), nullable=False)
    position = Column(Integer)
    added_at = Column(DateTime(timezone=True), default=utc_now)
    
    # Relationships
    playlist = relationship("Playlist", back_populates="playlist_videos")
    video = relationship("Video", back_populates="playlist_videos")

class Subscription(Base):
    __tablename__ = "subscriptions"
    
    id = Column(Integer, primary_key=True, index=True)
    subscriber_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    channel_id = Column(Integer, ForeignKey("channels.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), default=utc_now)
    
    # Relationships
    subscriber = relationship("User", foreign_keys=[subscriber_id], back_populates="subscriptions")
    channel = relationship("Channel", foreign_keys=[channel_id], back_populates="subscriptions")

class ModerationLog(Base):
    __tablename__ = "moderation_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    video_id = Column(Integer, ForeignKey("videos.id"))
    content_type = Column(String(20))
    status = Column(String(20))
    ai_score = Column(JSON)
    reviewed_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    reviewed_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), default=utc_now)
    notes = Column(Text)
