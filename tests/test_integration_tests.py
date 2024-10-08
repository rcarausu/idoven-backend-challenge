import time

from fastapi.testclient import TestClient

from src.insights.application.service.process_insights_service import ProcessInsightsService
from src.dependencies import register_ecg_service, register_user_service, get_insights_service, process_insights_service
from src.ecg.adapter.out_adapters.persistence.in_memory_ecg_persistence_adapter import InMemoryEcgPersistenceAdapter
from src.ecg.application.service.register_ecg_service import RegisterEcgService
from src.insights.adapter.out_adapters.persistence.in_memory_insights_persistence_adapter import \
    InMemoryInsightsPersistenceAdapter
from src.insights.application.service.get_insights_service import GetInsightsService
from src.main import app
from src.user.adapter.out_adapters.in_memory_user_persistence_adapter import InMemoryUserPersistenceAdapter
from src.user.application.port.in_ports.register_user_use_case import AdminToken
from src.user.application.service.register_user_service import RegisterUserService

client = TestClient(app)


class TestIntegrationTests:
    in_memory_ecg_adapter = InMemoryEcgPersistenceAdapter({})
    in_memory_user_adapter = InMemoryUserPersistenceAdapter({})
    in_memory_insights_adapter = InMemoryInsightsPersistenceAdapter({})

    def setup_method(self):
        app.dependency_overrides[register_user_service] = lambda: RegisterUserService(
            self.in_memory_user_adapter, AdminToken("token")
        )
        app.dependency_overrides[register_ecg_service] = lambda: RegisterEcgService(
            self.in_memory_ecg_adapter, self.in_memory_user_adapter, self.in_memory_insights_adapter
        )
        app.dependency_overrides[get_insights_service] = lambda: GetInsightsService(
            self.in_memory_ecg_adapter, self.in_memory_user_adapter, self.in_memory_insights_adapter
        )
        app.dependency_overrides[process_insights_service] = lambda: ProcessInsightsService(
            self.in_memory_insights_adapter
        )

    @staticmethod
    def teardown_method():
        app.dependency_overrides = {}

    def test_full_create_user_register_ecg_and_retrieve_insights_flow(self):
        health_response = client.get("/health/ping")
        # then
        assert health_response.status_code == 200
        assert health_response.json() == "pong"

        user_result = client.post("/users", headers={"x-admin-token": "token"}, json={"username": "user"})

        assert user_result.status_code == 201

        user_token = user_result.json()['token']

        ecg_result = client.post("/ecgs", headers={"x-user-token": user_token},
                                 json={"leads": [{"name": "I", "signal": [1, 0, -1]}]})

        assert ecg_result.status_code == 201

        ecg_id = ecg_result.json()["id"]

        # sleeping to ensure background processing is done
        time.sleep(1)

        insights_result = client.get(f"ecgs/{ecg_id}/insights", headers={"x-user-token": user_token})

        assert insights_result.status_code == 200
        assert insights_result.json()['leads'] == [
            {
                "name": "I",
                "number_of_zero_crossings": 1
            }
        ]
