from abc import ABCMeta, abstractmethod
from typing import Optional

from src.ecg.domain.ecg import ECG, EcgId


class GetEcgPort(metaclass=ABCMeta):
    @abstractmethod
    def get(self, ecg_id: EcgId) -> Optional[ECG]:
        raise NotImplementedError
