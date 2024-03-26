from abc import ABCMeta, abstractmethod
from typing import Optional

from src.ecg.domain.ecg import EcgId
from src.insights.domain.insights import Insights


class GetInsightsPort(metaclass=ABCMeta):
    @abstractmethod
    def get_by_ecg_id(self, ecg_id: EcgId) -> Optional[Insights]:
        raise NotImplementedError
