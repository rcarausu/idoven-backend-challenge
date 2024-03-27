from typing import Optional

from src.ecg.domain.ecg import EcgId
from src.insights.domain.insights import Insights, InsightsId
from src.insights.application.port.out_ports.get_insights_port import GetInsightsPort
from src.insights.application.port.out_ports.save_insights_port import SaveInsightsPort


class InMemoryInsightsPersistenceAdapter(GetInsightsPort, SaveInsightsPort):

    def __init__(self, repository: dict):
        self.__repository = repository

    def get_by_ecg_id(self, ecg_id: EcgId) -> Optional[Insights]:
        # O(n) retrieval time since we have to iterate through all keys in the worst case
        for insight_id in self.__repository.keys():
            if self.__repository[insight_id].ecg_id == ecg_id:
                return self.__repository[insight_id]
        return None

    def save(self, insights: Insights) -> InsightsId:
        # O(n) insertion since we need to iterate to find any possible duplicates and overwrite them, since
        #  insights should be unique per ecg_id
        for insight_id in self.__repository.keys():
            current_insights = self.__repository[insight_id]
            if current_insights.ecg_id == insights.ecg_id:
                updated_insights = Insights(
                    id=current_insights.id,
                    ecg_id=current_insights.ecg_id,
                    create_date=current_insights.create_date,
                    leads=insights.leads,
                    status=insights.status
                )
                self.__repository[insight_id] = updated_insights
                return updated_insights.id
        self.__repository[insights.id.value] = insights
        return insights.id
