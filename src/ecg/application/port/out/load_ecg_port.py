from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from typing import Optional

from ecg.domain.ecg import ECG, EcgId


@dataclass
class LoadEcgQuery:
    ecg_id: EcgId


class LoadEcgPort(metaclass=ABCMeta):
    @abstractmethod
    def load(self, query: LoadEcgQuery) -> Optional[ECG]:
        raise NotImplementedError
