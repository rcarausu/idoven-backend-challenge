from abc import ABCMeta, abstractmethod

from src.ecg.domain.user import UserId
from src.ecg.domain.ecg import ECG, EcgId


class SaveEcgPort(metaclass=ABCMeta):

    @abstractmethod
    def save(self, ecg: ECG) -> EcgId:
        raise NotImplementedError
