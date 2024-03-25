from abc import ABCMeta, abstractmethod
from typing import Optional

from src.ecg.domain.ecg import ECG, EcgId


class EcgNotFoundError(Exception):
    def __init__(self, ecg_id: EcgId):
        self.message = f"ECG not found for id {ecg_id.value}"
        super().__init__(self.message)


class GetEcgPort(metaclass=ABCMeta):
    @abstractmethod
    def get(self, ecg_id: EcgId) -> Optional[ECG]:
        raise NotImplementedError
