from src.ecg.application.port.out_ports.get_user_port import GetUserPort
from src.ecg.application.port.in_ports.register_ecg_use_case import RegisterEcgUseCase, RegisterEcgCommand
from src.ecg.application.port.in_ports.errors import InvalidUserTokenError
from src.ecg.application.port.out_ports.save_ecg_port import SaveEcgPort
from src.ecg.domain.ecg import EcgId, ECG


class RegisterEcgService(RegisterEcgUseCase):

    def __init__(self, save_ecg_port: SaveEcgPort, get_user_port: GetUserPort):
        self._save_ecg_port = save_ecg_port
        self._get_user_port = get_user_port

    def register_ecg(self, command: RegisterEcgCommand) -> EcgId:
        user = self._get_user_port.get_by_token(command.user_token)
        if not user:
            raise InvalidUserTokenError()
        ecg = ECG(
            user_id=user.id,
            leads=command.leads
        )
        return self._save_ecg_port.save(ecg)
