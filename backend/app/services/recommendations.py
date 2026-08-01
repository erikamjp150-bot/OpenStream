from typing import List, Dict, Any


class RecommendationService:
    def __init__(self) -> None:
        self.seed_videos = [
            {"id": 1, "title": "OpenStream Foundations", "description": "Build a transparent video platform", "category": "technology"},
            {"id": 2, "title": "Community Moderation Playbook", "description": "How to run humane review flows", "category": "community"},
            {"id": 3, "title": "Open Source Media Week", "description": "A look at creator-first platforms", "category": "opensource"},
        ]

    def recommend_for_user(self, user_profile: Dict[str, Any], limit: int = 5) -> List[Dict[str, Any]]:
        likes = set(user_profile.get("likes", []))
        history = set(user_profile.get("watch_history", []))
        ranked = []
        for video in self.seed_videos:
            score = 0
            if any(keyword in video["category"].lower() for keyword in likes):
                score += 2
            if any(keyword in video["title"].lower() for keyword in history):
                score += 1
            ranked.append((score, video))
        ranked.sort(key=lambda item: item[0], reverse=True)
        return [item[1] for item in ranked[:limit]]
