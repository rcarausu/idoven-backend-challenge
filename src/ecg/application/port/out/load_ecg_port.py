from abc import ABCMeta, abstractmethod
from typing import Optional

from ecg.domain.ecg import ECG, EcgId


class LoadECGPort(metaclass=ABCMeta):
    @abstractmethod
    def load(self, ecg_id: EcgId) -> Optional[ECG]:
        raise NotImplementedError
