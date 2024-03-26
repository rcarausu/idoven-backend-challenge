from unittest.mock import Mock, patch

from src.insights.domain.insights import InsightsId
from src.ecg.domain.ecg import EcgId, Lead
from src.insights.application.port.out_ports.process_insights_use_case import ProcessInsightsCommand
from src.insights.application.port.out_ports.save_insights_port import SaveInsightsPort
from src.insights.application.service.process_insights_service import ProcessInsightsService


class TestProcessInsightsService:

    mocked_save_insights_port: SaveInsightsPort = Mock(spec=SaveInsightsPort)

    service = ProcessInsightsService(mocked_save_insights_port)

    def test_it_should_calculate_number_of_zero_crossings(self):
        # when
        result = ProcessInsightsService._number_of_zero_crossings([1, -2, 0, 3, -4, 0, 0, 5, 6, -7])
        # then
        assert result == 5

    def test_it_should_process_insights(self):
        # given
        leads = [Lead('V1', signal=[1, -2, 0, 3, -4, 0, 0, 5, 6, -7])]
        command = ProcessInsightsCommand(EcgId(), leads)
        # when
        self.mocked_save_insights_port.save.return_value = InsightsId("id")
        result = self.service.process_insights(command)
        # then
        assert result == InsightsId("id")
