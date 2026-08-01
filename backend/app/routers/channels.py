from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Channel, User
from ..schemas import ChannelResponse

router = APIRouter()

@router.get("/{channel_id}", response_model=ChannelResponse)
async def get_channel(channel_id: int, db: Session = Depends(get_db)):
    channel = db.query(Channel).filter(Channel.id == channel_id).first()
    if not channel:
        raise HTTPException(status_code=404, detail="Channel not found")
    return channel

@router.get("/", response_model=list[ChannelResponse])
async def list_channels(db: Session = Depends(get_db)):
    return db.query(Channel).all()
