from src.ecg.application.port.in_ports.load_ecg_insights_use_case import LoadEcgInsightsUseCase, LoadEcgInsightsQuery
from src.ecg.application.port.out_ports.get_ecg_port import GetEcgPort, EcgNotFoundError
from src.ecg.domain.insights import Insights, Insight


class LoadEcgInsightsService(LoadEcgInsightsUseCase):

    def __init__(self, port: GetEcgPort):
        self._port = port

    def get_insights(self, query: LoadEcgInsightsQuery) -> Insights:
        ecg = self._port.get(query.id)

        if ecg is None:
            raise EcgNotFoundError(query.id)

        return Insights(
            [Insight(lead.name, lead.number_of_zero_crossings()) for lead in ecg.leads]
        )
