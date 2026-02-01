import pytest
from src.services.redis import get_redis_client


class TestRedis:
    """Test Redis connection."""

    def test_redis_ping(self):
        """Test that Redis connection is successful."""
        client = get_redis_client()
        result = client.ping()
        if not result:
            pytest.skip("Redis not reachable - skipping test (use local Redis or Railway public URL)")
        assert result is True
