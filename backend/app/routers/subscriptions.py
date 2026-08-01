from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Subscription

router = APIRouter()

@router.post("/", status_code=201)
async def subscribe(channel_id: int, db: Session = Depends(get_db)):
    subscription = Subscription(channel_id=channel_id, subscriber_id=1)
    db.add(subscription)
    db.commit()
    return {"ok": True}
