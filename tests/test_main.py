from fastapi.testclient import TestClient
from src.main import app

def test_status():
    client = TestClient(app)
    response = client.get("/status")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}