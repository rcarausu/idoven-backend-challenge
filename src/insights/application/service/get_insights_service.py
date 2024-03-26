from src.ecg.application.port.out_ports.errors import EcgNotFoundError
from src.ecg.application.port.out_ports.get_ecg_port import GetEcgPort
from src.insights.application.port.in_ports.errors import InsightsNotFoundError
from src.insights.application.port.in_ports.get_insights_use_case import GetInsightsUseCase, \
    GetInsightsQuery
from src.insights.application.port.out_ports.get_insights_port import GetInsightsPort
from src.insights.domain.insights import Insights
from src.user.application.port.in_ports.errors import InvalidUserTokenError
from src.user.application.port.out_ports.get_user_port import GetUserPort


class GetInsightsService(GetInsightsUseCase):

    def __init__(self, get_ecg_port: GetEcgPort, get_user_port: GetUserPort, get_insights_port: GetInsightsPort):
        self._get_ecg_port = get_ecg_port
        self._get_user_port = get_user_port
        self._get_insights_port = get_insights_port

    def get_insights(self, query: GetInsightsQuery) -> Insights:
        user = self._get_user_port.get_by_token(query.user_token)

        if not user:
            raise InvalidUserTokenError()

        ecg = self._get_ecg_port.get(query.ecg_id)

        if ecg is None or ecg.user_id != user.id:
            raise EcgNotFoundError(query.ecg_id)

        insights = self._get_insights_port.get_by_ecg_id(ecg.id)

        if not insights:
            raise InsightsNotFoundError(ecg.id)

        return insights
