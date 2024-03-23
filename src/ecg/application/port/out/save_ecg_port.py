from abc import ABCMeta, abstractmethod
from dataclasses import dataclass

from ecg.domain.ecg import ECG, EcgId


@dataclass
class SaveEcgCommand:
    ecg: ECG


class SaveEcgPort(metaclass=ABCMeta):

    @abstractmethod
    def save(self, command: SaveEcgCommand) -> EcgId:
        raise NotImplementedError
