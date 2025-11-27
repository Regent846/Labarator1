import pytest
import requests

@pytest.mark.smoke
class TestHealthCheck:
    def test_health_endpoint_returns_200(self, api_client):
        """Проверка, что эндпоинт /posts доступен."""
        response = api_client.get("/posts")
        assert response.status_code == 200

    def test_response_structure(self, api_client):
        """Проверка структуры ответа (должен быть список)."""
        response = api_client.get("/posts")
        assert isinstance(response.json(), list)
        assert len(response.json()) > 0