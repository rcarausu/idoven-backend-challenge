from abc import abstractmethod, ABCMeta
from dataclasses import dataclass

from src.ecg.domain.ecg import EcgId, ECG


@dataclass
class RegisterEcgCommand:
    ecg: ECG


class RegisterEcgUseCase(metaclass=ABCMeta):

    @abstractmethod
    def register_ecg(self, command: RegisterEcgCommand) -> EcgId:
        pass
