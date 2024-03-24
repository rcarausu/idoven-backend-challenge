from unittest.mock import Mock, patch

from fastapi.testclient import TestClient

from src.ecg.application.service.register_ecg_service import RegisterEcgService
from src.main import app


class TestEcgRouter:
    client = TestClient(app)

    @staticmethod
    def mocked_register_ecg_service() -> RegisterEcgService:
        return Mock(spec=RegisterEcgService)

    def setup_method(self):
        app.dependency_overrides["register_ecg_service"] = self.mocked_register_ecg_service()

    @staticmethod
    def teardown_method():
        app.dependency_overrides = {}

    @patch('src.ecg.domain.ecg.uuid.uuid4', return_value="uuid4_generated_id")
    def test_it_registers_ecg(self, mocker):
        # when
        response = self.client.post(
            "/ecg",
            json={
                "leads": [
                    {
                        "name": "I",
                        "number_of_samples": 3,
                        "signal": [1, 0, -1]
                    }
                ]
            }
        )
        # then
        assert response.status_code == 201
        assert response.json() == {"id": "uuid4_generated_id"}
