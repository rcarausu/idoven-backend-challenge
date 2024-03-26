from typing import List

from src.insights.application.port.out_ports.process_insights_use_case import ProcessInsightsCommand
from src.insights.application.port.out_ports.process_insights_use_case import ProcessInsightsUseCase
from src.insights.application.port.out_ports.save_insights_port import SaveInsightsPort
from src.insights.domain.insights import Insights, Insight, InsightsId, InsightsStatus


class ProcessInsightsService(ProcessInsightsUseCase):

    def __init__(self, port: SaveInsightsPort):
        self._port = port

    @staticmethod
    def _number_of_zero_crossings(signal: List[int]) -> int:
        crossings = 0
        if len(signal) in (0, 1):
            return crossings
        previous_value = signal[0]
        for value in signal[1::]:
            if value == 0:
                if previous_value != 0:
                    crossings += 1
            elif value * previous_value < 0:
                crossings += 1
            previous_value = value
        return crossings

    def process_insights(self, command: ProcessInsightsCommand) -> InsightsId:
        leads = []
        for lead in command.leads:
            leads.append(
                Insight(
                    lead.name,
                    number_of_zero_crossings=self._number_of_zero_crossings(lead.signal)
                )
            )
        return self._port.save(Insights(command.ecg_id, leads, InsightsStatus.DONE))
