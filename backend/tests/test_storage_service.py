import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.services.storage import StorageService


def test_generate_signed_url_returns_accessible_url_for_local_file(tmp_path):
    storage = StorageService(base_dir=str(tmp_path))
    media_path = tmp_path / "demo.mp4"
    media_path.write_bytes(b"demo")

    signed_url = storage.generate_signed_url(str(media_path), expires=3600)

    assert signed_url is not None
    assert str(media_path) in signed_url or "demo.mp4" in signed_url
