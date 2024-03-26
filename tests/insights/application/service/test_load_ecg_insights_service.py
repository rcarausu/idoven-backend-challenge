from datetime import datetime
from unittest.mock import Mock

import pytest
from freezegun import freeze_time

from src.user.application.port.out_ports.get_user_port import GetUserPort
from src.user.domain.user import UserId, UserToken, User
from src.insights.application.port.in_ports.load_ecg_insights_use_case import LoadEcgInsightsQuery
from src.ecg.application.port.out_ports.get_ecg_port import GetEcgPort, EcgNotFoundError
from src.insights.application.service.load_ecg_insights_service import LoadEcgInsightsService
from src.insights.domain.insights import Insights, Insight
from src.ecg.domain.ecg import EcgId, ECG, Lead


class TestLoadEcgInsightsService:
    mocked_ecg_port: GetEcgPort = Mock(spec=GetEcgPort)
    mocked_user_port: GetUserPort = Mock(spec=GetUserPort)

    service = LoadEcgInsightsService(mocked_ecg_port, mocked_user_port)

    def test_it_should_raise_not_found_error_if_ecg_is_not_found(self):
        # given
        ecg_id = EcgId("id")
        self.mocked_ecg_port.get.return_value = None
        self.mocked_user_port.get_by_token.return_value = User("user")
        # when
        with pytest.raises(EcgNotFoundError) as e:
            self.service.get_insights(LoadEcgInsightsQuery(ecg_id, UserToken()))
        # then
        assert e.value.message == "ECG not found for id id"

    def test_it_should_raise_not_found_error_if_ecg_user_id_and_user_token_do_not_match(self):
        # given
        ecg_id = EcgId("id")
        self.mocked_ecg_port.get.return_value = ECG(user_id=UserId("id"))
        self.mocked_user_port.get_by_token.return_value = User("user", UserId("different_id"))
        # when
        with pytest.raises(EcgNotFoundError) as e:
            self.service.get_insights(LoadEcgInsightsQuery(ecg_id, UserToken()))
        # then
        assert e.value.message == "ECG not found for id id"

    @freeze_time()
    def test_it_should_load_insights(self):
        # given
        ecg_id = EcgId("id")
        self.mocked_ecg_port.get.return_value = ECG(
            id=ecg_id,
            user_id=UserId("id"),
            create_date=datetime(2024, 1, 1),
            leads=[
                Lead('I', signal=[-1, 0, 1, 2, 1, 0, -1, 0, 0, 1]),
                Lead('II', signal=[1, 2, 3])
            ]
        )
        self.mocked_user_port.get_by_token.return_value = User("user", UserId("id"))
        # when
        result = self.service.get_insights(LoadEcgInsightsQuery(ecg_id, UserToken()))
        # then
        assert result == Insights(
            ecg_id,
            leads=[
                Insight('I', 3),
                Insight('II', 0)
            ]
        )
