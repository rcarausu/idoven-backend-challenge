
from abc import abstractmethod, ABCMeta
from dataclasses import dataclass

from ecg.domain.ecg import EcgId
from ecg.domain.insights import Insights


@dataclass
class LoadEcgInsightsQuery:
    id: EcgId


class LoadEcgInsightsUseCase(metaclass=ABCMeta):

    @abstractmethod
    def get_insights(self, query: LoadEcgInsightsQuery) -> Insights:
        pass
