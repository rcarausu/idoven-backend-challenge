import pytest

from src.user.application.port.in_ports.register_user_use_case import AdminToken
from src.user.application.port.in_ports.errors import InvalidAdminTokenError
from src.user.application.port.out_ports.save_user_port import SaveUserPort
from src.user.application.service.register_user_service import RegisterUserCommand, RegisterUserService

from unittest.mock import Mock

from src.user.domain.user import UserId, User


class TestRegisterUserService:

    token = AdminToken("token")
    mocked_port = Mock(spec=SaveUserPort)

    service = RegisterUserService(mocked_port, token)

    def test_it_raises_error_if_admin_not_authenticated(self):
        # when
        with pytest.raises(InvalidAdminTokenError) as e:
            self.service.register_user(RegisterUserCommand(AdminToken("bad_token"), User("username")))
        # then
        assert e.value.message == "Invalid admin token"

    def test_it_should_register_user(self):
        # given
        self.mocked_port.save.return_value = UserId("id")
        # when
        result = self.service.register_user(RegisterUserCommand(AdminToken("token"), User("username", UserId("id"))))
        # then
        assert result == UserId("id")
