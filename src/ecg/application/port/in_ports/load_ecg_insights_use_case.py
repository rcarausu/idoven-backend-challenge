from abc import abstractmethod, ABCMeta
from dataclasses import dataclass

from src.ecg.domain.user import UserToken
from src.ecg.domain.ecg import EcgId
from src.ecg.domain.insights import Insights


@dataclass
class LoadEcgInsightsQuery:
    id: EcgId
    user_token: UserToken


class LoadEcgInsightsUseCase(metaclass=ABCMeta):

    @abstractmethod
    def get_insights(self, query: LoadEcgInsightsQuery) -> Insights:
        pass
