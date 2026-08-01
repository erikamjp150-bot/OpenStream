import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.services.moderation import ContentModerator
from app.services.recommendations import RecommendationService


def test_moderation_recommendation_services_boot():
    moderator = ContentModerator()
    service = RecommendationService()

    payload = moderator.score_video("safe content", "")
    assert payload["status"] in {"approved", "review"}

    user_profile = {"likes": ["tech", "opensource"], "watch_history": ["python", "docker"]}
    recommendations = service.recommend_for_user(user_profile, limit=3)
    assert len(recommendations) <= 3
    assert all("title" in item for item in recommendations)
