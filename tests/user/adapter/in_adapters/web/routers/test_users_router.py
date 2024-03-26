from unittest.mock import Mock, patch

from fastapi.testclient import TestClient

from src.dependencies import register_user_service
from src.user.application.port.in_ports.register_user_use_case import InvalidAdminTokenError
from src.user.application.service.register_user_service import RegisterUserService
from src.user.domain.user import UserId
from src.main import app

client = TestClient(app)


class TestRegisterUserRouter:
    mocked_service: RegisterUserService = Mock(spec=RegisterUserService)

    def mocked_register_user_service(self) -> RegisterUserService:
        return self.mocked_service

    def setup_method(self):
        app.dependency_overrides[register_user_service] = self.mocked_register_user_service

    def teardown_method(self):
        # resetting side effect of mocked object, otherwise it's propagated to other test cases
        self.mocked_service.register_user.side_effect = None
        app.dependency_overrides = {}

    def test_it_returns_unauthorized_if_admin_token_is_wrong(self):
        # given
        self.mocked_service.register_user.side_effect = InvalidAdminTokenError()
        # when
        response = client.post("/users", headers={"x-admin-token": ""}, json={"username": "user"})
        # then
        assert response.status_code == 401
        assert response.json() == {
            "message": "Invalid admin token"
        }

    @patch('src.user.domain.user.uuid.uuid4', return_value="uuid4_generated_token")
    def test_it_registers_user(self, mocker):
        # given
        self.mocked_service.register_user.return_value = UserId("id")
        # when
        response = client.post("/users", headers={"x-admin-token": "token"}, json={"username": "user"})
        # then
        assert response.status_code == 201
        assert response.json() == {
            "username": "user",
            "token": "uuid4_generated_token"
        }
