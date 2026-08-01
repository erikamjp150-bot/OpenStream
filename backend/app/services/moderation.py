from typing import Dict, Any


class ContentModerator:
    def __init__(self) -> None:
        self.rules = {
            "safe": ["open", "source", "community"],
            "flag": ["violence", "hate", "explicit"],
        }

    def score_video(self, title: str, description: str) -> Dict[str, Any]:
        text = f"{title} {description}".lower()
        if any(word in text for word in self.rules["flag"]):
            return {"status": "review", "score": 0.7, "reason": "flagged keywords"}
        return {"status": "approved", "score": 0.95, "reason": "safe content"}

    async def moderate_video(self, video_id: int, video_url: str, thumbnail_url: str) -> Dict[str, Any]:
        result = self.score_video(video_url, thumbnail_url)
        return {"video_id": video_id, **result}
