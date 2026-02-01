from fastapi.testclient import TestClient
from src.main import app


class TestMain:
    """Test main application endpoints."""

    def test_status(self):
        """Test that status endpoint returns ok."""
        client = TestClient(app)
        response = client.get("/status")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}