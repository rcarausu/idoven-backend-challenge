from abc import abstractmethod, ABCMeta
from dataclasses import dataclass

from src.ecg.application.port.in_ports.models.ecg_model import ECGModel
from src.ecg.domain.ecg import EcgId


@dataclass
class RegisterEcgCommand:
    ecg: ECGModel


class RegisterEcgUseCase(metaclass=ABCMeta):

    @abstractmethod
    def register_ecg(self, command: RegisterEcgCommand) -> EcgId:
        pass
