from unittest.mock import Mock, MagicMock

from fastapi.testclient import TestClient

from src.dependencies import register_ecg_service, get_insights_service
from src.user.application.port.in_ports.errors import InvalidUserTokenError
from src.ecg.application.port.out_ports.errors import EcgNotFoundError
from src.insights.application.service.get_insights_service import GetInsightsService
from src.ecg.application.service.register_ecg_service import RegisterEcgService
from src.ecg.domain.ecg import EcgId
from src.insights.domain.insights import Insights, Insight, InsightsStatus
from src.main import app

client = TestClient(app)


class TestRegisterEcgRouter:
    mocked_service: RegisterEcgService = Mock(spec=RegisterEcgService)

    def mocked_register_ecg_service(self) -> RegisterEcgService:
        return self.mocked_service

    def setup_method(self):
        app.dependency_overrides[register_ecg_service] = self.mocked_register_ecg_service

    def teardown_method(self):
        # resetting side effect of mocked object, otherwise it's propagated to other test cases
        self.mocked_service.register_ecg.side_effect = None
        app.dependency_overrides = {}

    def test_it_returns_unauthorized_if_user_token_is_invalid(self):
        # given
        self.mocked_service.register_ecg.side_effect = InvalidUserTokenError()
        # when
        response = client.post(
            "/ecgs",
            headers={"x-user-token": "bad-token"},
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
        assert response.status_code == 401
        assert response.json() == {"detail": "Invalid user token"}

    def test_it_registers_ecg(self):
        # given
        self.mocked_service.register_ecg.return_value = EcgId("uuid4_generated_id")
        # when
        response = client.post(
            "/ecgs",
            headers={"x-user-token": "user-token"},
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


class TestGetInsightsRouter:
    mocked_service: GetInsightsService = MagicMock(spec=GetInsightsService)

    def mocked_load_ecg_insights_service(self) -> GetInsightsService:
        return self.mocked_service

    def setup_method(self):
        app.dependency_overrides[get_insights_service] = self.mocked_load_ecg_insights_service

    def teardown_method(self):
        # resetting side effect of mocked object, otherwise it's propagated to other test cases
        self.mocked_service.get_insights.side_effect = None
        app.dependency_overrides = {}

    def test_it_returns_not_found_if_ecg_does_not_exist(self):
        # given
        self.mocked_service.get_insights.side_effect = EcgNotFoundError(EcgId("uuid4_generated_id"))
        # when
        response = client.get("/ecgs/uuid4_generated_id/insights", headers={"x-user-token": ""})
        # then
        assert response.status_code == 404
        assert response.json() == {
            "detail": "ECG not found for id uuid4_generated_id"
        }

    def test_it_returns_unauthorized_if_token_is_invalid(self):
        # given
        self.mocked_service.get_insights.side_effect = InvalidUserTokenError()
        # when
        response = client.get("/ecgs/uuid4_generated_id/insights", headers={"x-user-token": ""})
        # then
        assert response.status_code == 401
        assert response.json() == {
            "detail": "Invalid user token"
        }

    def test_it_returns_accepted_if_insights_are_still_being_processed(self):
        # given
        self.mocked_service.get_insights.return_value = Insights(
            EcgId("id"),
            status=InsightsStatus.IN_PROGRESS,
            leads=[
                Insight("I", 10),
                Insight("II", 2)
            ]
        )
        # when
        response = client.get("/ecgs/uuid4_generated_id/insights", headers={"x-user-token": ""})
        # then
        assert response.status_code == 202
        assert response.json() == {
            "detail": "Insights are still being processed"
        }

    def test_it_returns_insights(self):
        # given
        self.mocked_service.get_insights.return_value = Insights(
            EcgId("id"),
            status=InsightsStatus.DONE,
            leads=[
                Insight("I", 10),
                Insight("II", 2)
            ]
        )
        # when
        response = client.get("/ecgs/uuid4_generated_id/insights", headers={"x-user-token": ""})
        # then
        assert response.status_code == 200
        assert response.json() == {
            "ecg_id": "id",
            "leads": [
                {
                    "name": "I",
                    "number_of_zero_crossings": 10
                },
                {
                    "name": "II",
                    "number_of_zero_crossings": 2
                }
            ]
        }
