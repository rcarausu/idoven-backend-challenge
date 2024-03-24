from src.ecg.application.port.in_ports.models.ecg_model import as_ecg
from src.ecg.application.port.in_ports.register_ecg_use_case import RegisterEcgUseCase, RegisterEcgCommand
from src.ecg.application.port.out_ports.save_ecg_port import SaveEcgPort
from src.ecg.domain.ecg import EcgId


class RegisterEcgService(RegisterEcgUseCase):

    def __init__(self, port: SaveEcgPort):
        self._port = port

    def register_ecg(self, command: RegisterEcgCommand) -> EcgId:
        ecg = as_ecg(command.ecg)
        return self._port.save(ecg)
