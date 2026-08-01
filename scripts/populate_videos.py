#!/usr/bin/env python
"""
Script to populate OpenStream with sample videos.
Place sample video files in /sample_videos/ directory.
"""

import os
import sys
import random
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
import requests
import json

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))
from app.models import User, Channel, Video
from app.config import settings
from app.services.video_processor import VideoProcessor
from app.services.storage import StorageService

# Database connection
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_sample_channel(session, username, email, channel_name):
    """Create a sample user and channel"""
    user = User(
        username=username,
        email=email,
        hashed_password="dummy_hash",  # Not used for sample
        full_name=f"Sample {username}",
        is_active=True
    )
    session.add(user)
    session.commit()
    
    channel = Channel(
        user_id=user.id,
        name=channel_name,
        description=f"Sample channel for {channel_name}",
        subscriber_count=random.randint(100, 10000)
    )
    session.add(channel)
    session.commit()
    
    return channel

def create_sample_video(session, channel, title, description, video_path):
    """Create a sample video from a file"""
    if not os.path.exists(video_path):
        print(f"Video file not found: {video_path}")
        return None
    
    processor = VideoProcessor()
    storage = StorageService()
    
    try:
        # Process video
        processed = processor.process_video(video_path)
        
        # Upload to storage
        video_url = storage.upload_file(
            processed['output_path'],
            f"videos/{channel.id}/{processed['video_id']}.mp4",
            content_type="video/mp4"
        )
        thumbnail_url = storage.upload_file(
            processed['thumbnail_path'],
            f"thumbnails/{channel.id}/{processed['video_id']}.jpg",
            content_type="image/jpeg"
        )
        
        # Create video record
        video = Video(
            channel_id=channel.id,
            title=title,
            description=description,
            video_url=video_url,
            thumbnail_url=thumbnail_url,
            duration=processed['metadata']['duration'],
            width=processed['metadata']['width'],
            height=processed['metadata']['height'],
            file_size=processed['metadata']['file_size'],
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
        
    except Exception as e:
        print(f"❌ Failed to create video: {e}")
        session.rollback()
        return None

def main():
    """Main script to populate videos"""
    session = SessionLocal()
    
    # Sample video directory
    sample_dir = os.path.join(os.path.dirname(__file__), '..', 'sample_videos')
    os.makedirs(sample_dir, exist_ok=True)
    
    print("📹 OpenStream Video Population Script")
    print("=" * 40)
    print(f"Place sample video files in: {sample_dir}")
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
    
    # Create videos (if files exist)
    for idx, data in enumerate(sample_data):
        video_path = os.path.join(sample_dir, data['file'])
        channel = channels[idx % len(channels)]
        
        create_sample_video(
            session,
            channel,
            data['title'],
            data['description'],
            video_path
        )
    
    print("")
    print("✅ Population complete!")
    print("If no videos were created, ensure you have sample files in the sample_videos/ directory.")
    print("You can also manually upload videos through the web interface.")
    
    session.close()

if __name__ == "__main__":
    main()
