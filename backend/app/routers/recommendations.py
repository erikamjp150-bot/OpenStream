from fastapi import APIRouter
from ..services.recommendations import RecommendationService

router = APIRouter()
service = RecommendationService()


@router.get("/")
def list_recommendations():
    return service.recommend_for_user({"likes": ["tech", "opensource"], "watch_history": ["python", "docker"]}, limit=3)
