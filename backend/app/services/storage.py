from pathlib import Path
from typing import Optional
from datetime import timedelta


class StorageService:
    def __init__(self, base_dir: Optional[str] = None) -> None:
        self.base_dir = Path(base_dir or "/tmp/openstream_storage")
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def upload_file(self, source_path: str, destination_path: str, content_type: Optional[str] = None) -> str:
        destination = self.base_dir / destination_path
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(Path(source_path).read_bytes())
        return str(destination)

    def generate_signed_url(self, object_path: str, expires: int = 3600) -> str:
        path = Path(object_path)
        if not path.exists():
            return str(path)

        return str(path)
