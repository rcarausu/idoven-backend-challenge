from abc import ABCMeta, abstractmethod

from src.insights.domain.insights import Insights, InsightsId


class SaveInsightsPort(metaclass=ABCMeta):
    @abstractmethod
    def save(self, insights: Insights) -> InsightsId:
        raise NotImplementedError
