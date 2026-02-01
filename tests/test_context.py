"""Tests for deployment context API."""
import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient

from src.main import app


class TestDeploymentContext:
    """Test deployment context endpoints."""

    @pytest.fixture
    def client(self):
        """Create test client."""
        return TestClient(app)

    @pytest.fixture
    def mock_redis(self):
        """Mock Redis client."""
        with patch("src.routers.day0_identity_topology.context.get_redis_client") as mock:
            redis_mock = MagicMock()
            mock.return_value = redis_mock
            yield redis_mock

    @pytest.fixture
    def sample_context(self):
        """Sample deployment context data."""
        return {
            "api_host": "api.mist.com",
            "org_id": "test-org-123",
            "ssr1_mac": "aa:bb:cc:dd:ee:01",
            "ssr2_mac": "aa:bb:cc:dd:ee:02",
            "ex1_mac": "aa:bb:cc:dd:ee:03",
            "ap1_mac": "aa:bb:cc:dd:ee:04",
            "mgmt_vlan": 100,
            "vlan_1": 200,
            "vlan_2": 300
        }

    def test_get_context_found(self, client, mock_redis, sample_context):
        """Test retrieving existing deployment context."""
        import json
        mock_redis.get.return_value = json.dumps(sample_context)
        
        response = client.get("/context/")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "found"
        assert data["context"]["org_id"] == "test-org-123"
        assert data["context"]["mgmt_vlan"] == 100

    def test_get_context_not_found(self, client, mock_redis):
        """Test retrieving non-existent context."""
        mock_redis.get.return_value = None
        
        response = client.get("/context/")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "not_found"
        assert data["context"] is None

    def test_delete_context(self, client, mock_redis):
        """Test deleting deployment context."""
        mock_redis.delete.return_value = 1
        
        response = client.delete("/context/")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "deleted"
        mock_redis.delete.assert_called_once()
