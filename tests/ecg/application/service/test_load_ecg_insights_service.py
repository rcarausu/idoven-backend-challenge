from datetime import datetime
from unittest.mock import Mock

import pytest

from src.ecg.application.port.in_ports.load_ecg_insights_use_case import LoadEcgInsightsQuery
from src.ecg.application.port.out_ports.get_ecg_port import GetEcgPort, EcgNotFoundError
from src.ecg.application.service.load_ecg_insights_service import LoadEcgInsightsService
from src.ecg.domain.insights import Insights, Insight
from src.ecg.domain.ecg import EcgId, ECG, Lead


class TestLoadEcgInsightsService:
    mocked_port: GetEcgPort = Mock(spec=GetEcgPort)

    service = LoadEcgInsightsService(mocked_port)

    def test_it_should_raise_error_if_ecg_is_not_found(self):
        # given
        ecg_id = EcgId("id")
        self.mocked_port.get.return_value = None
        # when
        with pytest.raises(EcgNotFoundError) as e:
            self.service.get_insights(LoadEcgInsightsQuery(ecg_id))
        # then
        assert e.value.args[0] == "ECG not found for id id"

    def test_it_should_load_insights(self):
        # given
        ecg_id = EcgId("id")
        self.mocked_port.get.return_value = ECG(
            ecg_id,
            create_date=datetime(2024, 1, 1),
            leads=[
                Lead('I', signal=[-1, 0, 1, 2, 1, 0, -1, 0, 0, 1]),
                Lead('II', signal=[1, 2, 3])
            ]
        )
        # when
        result = self.service.get_insights(LoadEcgInsightsQuery(ecg_id))
        # then
        assert result == Insights(
            leads=[
                Insight('I', 3),
                Insight('II', 0)
            ]
        )
