from src.ecg.application.port.in_ports.register_user_use_case import RegisterUserCommand, RegisterUserUseCase, \
    InvalidAdminTokenError, AdminToken
from src.ecg.application.port.out_ports.save_user_port import SaveUserPort
from src.ecg.domain.user import UserId


class RegisterUserService(RegisterUserUseCase):

    def __init__(self, port: SaveUserPort, admin_token: AdminToken):
        self._port = port
        self._token = admin_token

    def register_user(self, command: RegisterUserCommand) -> UserId:
        if command.admin_token != self._token:
            raise InvalidAdminTokenError()
        return self._port.save(command.user)
