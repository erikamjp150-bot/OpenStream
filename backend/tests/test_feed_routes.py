import sys
from pathlib import Path

from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.main import app

client = TestClient(app)


def test_feed_root_route_returns_feed():
    response = client.get('/feed')
    assert response.status_code == 200
    payload = response.json()
    assert 'results' in payload
    assert 'total' in payload
