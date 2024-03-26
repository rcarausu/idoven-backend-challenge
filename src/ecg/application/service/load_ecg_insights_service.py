from src.ecg.application.port.in_ports.errors import InvalidUserTokenError
from src.ecg.application.port.in_ports.load_ecg_insights_use_case import LoadEcgInsightsUseCase, LoadEcgInsightsQuery
from src.ecg.application.port.out_ports.get_ecg_port import GetEcgPort, EcgNotFoundError
from src.user.application.port.out_ports.get_user_port import GetUserPort
from src.ecg.domain.insights import Insights, Insight


class LoadEcgInsightsService(LoadEcgInsightsUseCase):

    def __init__(self, get_ecg_port: GetEcgPort, get_user_port: GetUserPort):
        self._get_ecg_port = get_ecg_port
        self._get_user_port = get_user_port

    def get_insights(self, query: LoadEcgInsightsQuery) -> Insights:
        user = self._get_user_port.get_by_token(query.user_token)

        if not user:
            raise InvalidUserTokenError()

        ecg = self._get_ecg_port.get(query.id)

        if ecg is None or ecg.user_id != user.id:
            raise EcgNotFoundError(query.id)

        return Insights(
            [Insight(lead.name, lead.number_of_zero_crossings()) for lead in ecg.leads]
        )
