import sys
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts import populate_videos


def test_create_sample_video_uploads_real_thumbnail_file(tmp_path, monkeypatch):
    video_path = tmp_path / "clip.mp4"
    video_path.write_bytes(b"placeholder-video")

    thumbnail_path = tmp_path / "clip.jpg"
    thumbnail_path.write_bytes(b"fake-jpg")

    class DummyStorage:
        def __init__(self):
            self.calls = []

        def upload_file(self, source_path, destination_path, content_type=None):
            self.calls.append((source_path, destination_path))
            return f"/tmp/{destination_path}"

    storage = DummyStorage()
    monkeypatch.setattr(populate_videos, "StorageService", lambda: storage)

    class DummySession:
        def __init__(self):
            self.items = []

        def add(self, item):
            self.items.append(item)

        def commit(self):
            return None

        def rollback(self):
            return None

        def refresh(self, item):
            return None

    session = DummySession()
    channel = SimpleNamespace(id=7)

    result = populate_videos.create_sample_video(session, channel, "Sample title", "desc", str(video_path))

    assert result is not None
    assert len(storage.calls) == 2
    assert storage.calls[1][0] == str(thumbnail_path)
