#!/usr/bin/env python
"""
Script to populate OpenStream with sample videos.
Place sample video files in /sample_videos/ directory.
"""

import os
import sys
import random
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))
from app.models import User, Channel, Video
from app.config import settings
from app.services.storage import StorageService

# Database connection
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_sample_channel(session, username, email, channel_name):
    """Create a sample user and channel if it does not already exist."""
    existing_user = session.query(User).filter((User.username == username) | (User.email == email)).first()
    if existing_user:
        existing_channel = session.query(Channel).filter(Channel.user_id == existing_user.id).first()
        if existing_channel:
            return existing_channel
        channel = Channel(user_id=existing_user.id, name=channel_name, description=f"Sample channel for {channel_name}", subscriber_count=random.randint(100, 10000))
        session.add(channel)
        session.commit()
        return channel

    user = User(
        username=username,
        email=email,
        hashed_password="dummy_hash",
        full_name=f"Sample {username}",
        is_active=True,
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    channel = Channel(user_id=user.id, name=channel_name, description=f"Sample channel for {channel_name}", subscriber_count=random.randint(100, 10000))
    session.add(channel)
    session.commit()
    session.refresh(channel)
    return channel

def ensure_sample_media(sample_dir: Path):
    """Create a tiny placeholder video file when no real media exists."""
    sample_dir.mkdir(parents=True, exist_ok=True)
    for filename in ["intro.mp4", "future_oss.mp4", "contribute.mp4", "cc_explained.mp4"]:
        path = sample_dir / filename
        if not path.exists():
            path.write_bytes(b"placeholder-video")
            print(f"Created placeholder media: {path}")
    return sample_dir


def create_sample_video(session, channel, title, description, video_path):
    """Create a sample video record using a local placeholder asset."""
    storage = StorageService()
    sample_path = Path(video_path)
    if not sample_path.exists():
        print(f"Video file not found: {sample_path}")
        return None

    try:
        video_url = storage.upload_file(str(sample_path), f"videos/{channel.id}/{sample_path.stem}.mp4")
        thumbnail_url = storage.upload_file(str(sample_path), f"thumbnails/{channel.id}/{sample_path.stem}.jpg")

        video = Video(
            channel_id=channel.id,
            title=title,
            description=description,
            video_url=video_url,
            thumbnail_url=thumbnail_url,
            duration=45,
            width=1280,
            height=720,
            file_size=sample_path.stat().st_size,
            category=random.choice(['Education', 'Entertainment', 'Technology', 'Science']),
            tags=random.sample(['sample', 'demo', 'open-source'], 3),
            is_public=True,
            moderation_status='approved',
            published_at=datetime.now() - timedelta(days=random.randint(0, 30)),
            view_count=random.randint(100, 50000),
            like_count=random.randint(10, 5000),
            comment_count=random.randint(0, 200)
        )
        session.add(video)
        session.commit()

        print(f"✅ Created video: {title}")
        return video

    except Exception as exc:
        print(f"❌ Failed to create video: {exc}")
        session.rollback()
        return None

def main():
    """Main script to populate videos"""
    session = SessionLocal()
    
    sample_dir = Path(__file__).resolve().parent.parent / "sample_videos"
    ensure_sample_media(sample_dir)

    print("📹 OpenStream Video Population Script")
    print("=" * 40)
    print(f"Using sample asset folder: {sample_dir}")
    print("Supported formats: .mp4, .mov, .avi")
    print("")
    
    # Create sample channels
    channels = [
        create_sample_channel(session, "johnsmith", "john@example.com", "John's Tech Channel"),
        create_sample_channel(session, "janescience", "jane@example.com", "Science Unfolded"),
        create_sample_channel(session, "creativemind", "creative@example.com", "Creative Creations"),
    ]
    
    # Sample video data
    sample_data = [
        {
            "title": "Introduction to OpenStream",
            "description": "Welcome to OpenStream! Learn how this open-source platform works.",
            "file": "intro.mp4"
        },
        {
            "title": "The Future of Open Source",
            "description": "Exploring the impact of open-source software on the tech industry.",
            "file": "future_oss.mp4"
        },
        {
            "title": "How to Contribute to OpenStream",
            "description": "A step-by-step guide to contributing to this project.",
            "file": "contribute.mp4"
        },
        {
            "title": "Creative Commons Explained",
            "description": "Understanding open licenses and their importance.",
            "file": "cc_explained.mp4"
        }
    ]
    
    for idx, data in enumerate(sample_data):
        video_path = sample_dir / data['file']
        channel = channels[idx % len(channels)]
        create_sample_video(session, channel, data['title'], data['description'], str(video_path))
    
    print("")
    print("✅ Population complete!")
    print("Open the feed to see the new sample videos.")
    
    session.close()

if __name__ == "__main__":
    main()
