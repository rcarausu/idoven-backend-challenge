from abc import ABCMeta, abstractmethod

from ecg.domain.ecg import ECG, EcgId


class SaveECGPort(metaclass=ABCMeta):

    @abstractmethod
    def save(self, ecg: ECG) -> EcgId:
        raise NotImplementedError
