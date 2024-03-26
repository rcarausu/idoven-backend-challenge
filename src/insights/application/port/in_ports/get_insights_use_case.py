from abc import abstractmethod, ABCMeta
from dataclasses import dataclass

from src.user.domain.user import UserToken
from src.ecg.domain.ecg import EcgId
from src.insights.domain.insights import Insights


@dataclass
class GetInsightsQuery:
    ecg_id: EcgId
    user_token: UserToken


class GetInsightsUseCase(metaclass=ABCMeta):

    @abstractmethod
    def get_insights(self, query: GetInsightsQuery) -> Insights:
        pass
