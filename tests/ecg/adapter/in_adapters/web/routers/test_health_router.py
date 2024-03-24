from fastapi.testclient import TestClient

from src.main import app


class TestHealthRouter:
    client = TestClient(app)

    def test_health_check(self):
        # when
        response = self.client.get("/health/ping")
        # then
        assert response.status_code == 200
        assert response.json() == "pong"
