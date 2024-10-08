from unittest.mock import Mock

from src.ecg.application.port.in_ports.register_ecg_use_case import RegisterEcgCommand
from src.ecg.application.port.out_ports.save_ecg_port import SaveEcgPort
from src.ecg.application.service.register_ecg_service import RegisterEcgService
from src.ecg.domain.ecg import EcgId, Lead
from src.insights.application.port.out_ports.save_insights_port import SaveInsightsPort
from src.user.application.port.out_ports.get_user_port import GetUserPort
from src.user.domain.user import UserToken, User


class TestRegisterEcgService:
    mocked_save_ecg_port: SaveEcgPort = Mock(spec=SaveEcgPort)
    mocked_get_user_port: GetUserPort = Mock(spec=GetUserPort)
    mocked_insight_port: SaveInsightsPort = Mock(spec=SaveInsightsPort)

    service = RegisterEcgService(mocked_save_ecg_port, mocked_get_user_port, mocked_insight_port)

    def test_it_should_register_ecg(self):
        # given
        token = UserToken()
        leads = [
            Lead(
                name="I",
                number_of_samples=3,
                signal=[1, 0, -1]
            )
        ]

        self.mocked_save_ecg_port.save.return_value = EcgId("id")
        self.mocked_get_user_port.get_by_token.return_value = User("username")
        # when
        result = self.service.register_ecg(RegisterEcgCommand(token, leads))
        # then
        assert result == EcgId("id")
