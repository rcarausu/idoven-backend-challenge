from datetime import datetime
from unittest.mock import Mock, patch

import pytest
from freezegun import freeze_time

from src.ecg.application.port.out_ports.errors import EcgNotFoundError
from src.ecg.application.port.out_ports.get_ecg_port import GetEcgPort
from src.ecg.domain.ecg import EcgId, ECG, Lead
from src.insights.application.port.in_ports.errors import InsightsNotFoundError
from src.insights.application.port.in_ports.get_insights_use_case import GetInsightsQuery
from src.insights.application.port.out_ports.get_insights_port import GetInsightsPort
from src.insights.application.service.get_insights_service import GetInsightsService
from src.insights.domain.insights import Insights, Insight
from src.user.application.port.in_ports.errors import InvalidUserTokenError
from src.user.application.port.out_ports.get_user_port import GetUserPort
from src.user.domain.user import UserId, UserToken, User


class TestGetInsightsService:
    mocked_ecg_port: GetEcgPort = Mock(spec=GetEcgPort)
    mocked_user_port: GetUserPort = Mock(spec=GetUserPort)
    mocked_insights_port: GetInsightsPort = Mock(spec=GetInsightsPort)

    service = GetInsightsService(mocked_ecg_port, mocked_user_port, mocked_insights_port)

    def test_it_should_raise_invalid_user_token_error_if_user_is_not_found(self):
        # given
        ecg_id = EcgId("id")
        self.mocked_user_port.get_by_token.return_value = None
        # when
        with pytest.raises(InvalidUserTokenError) as e:
            self.service.get_insights(GetInsightsQuery(ecg_id, UserToken()))
        # then
        assert e.value.message == "Invalid user token"

    def test_it_should_raise_not_found_error_if_user_is_not_found(self):
        # given
        ecg_id = EcgId("id")
        self.mocked_ecg_port.get.return_value = None
        self.mocked_user_port.get_by_token.return_value = User("user")
        # when
        with pytest.raises(EcgNotFoundError) as e:
            self.service.get_insights(GetInsightsQuery(ecg_id, UserToken()))
        # then
        assert e.value.message == "ECG not found for id id"

    def test_it_should_raise_not_found_error_if_ecg_user_id_and_user_by_token_do_not_match(self):
        # given
        ecg_id = EcgId("id")
        self.mocked_ecg_port.get.return_value = ECG(user_id=UserId("id"))
        self.mocked_user_port.get_by_token.return_value = User("user", UserId("different_id"))
        # when
        with pytest.raises(EcgNotFoundError) as e:
            self.service.get_insights(GetInsightsQuery(ecg_id, UserToken()))
        # then
        assert e.value.message == "ECG not found for id id"

    @patch('src.insights.domain.insights.uuid.uuid4', return_value="uuid4_generated_id")
    def test_it_should_raise_insights_not_found_error_if_insights_not_found(self, mocker):
        # given
        ecg_id = EcgId("id")
        self.mocked_ecg_port.get.return_value = ECG(user_id=UserId("id"))
        self.mocked_user_port.get_by_token.return_value = User("user", UserId("id"))
        self.mocked_insights_port.get_by_ecg_id.return_value = None
        # when
        with pytest.raises(InsightsNotFoundError) as e:
            self.service.get_insights(GetInsightsQuery(ecg_id, UserToken()))
        # then
        assert e.value.message == "No insights found for ecg uuid4_generated_id"

    @freeze_time()
    @patch('src.insights.domain.insights.uuid.uuid4', return_value="uuid4_generated_id")
    def test_it_should_load_insights(self, mocker):
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
        self.mocked_insights_port.get_by_ecg_id.return_value = Insights(
            ecg_id,
            leads=[
                Insight('I', 3),
                Insight('II', 0)
            ]
        )
        # when
        result = self.service.get_insights(GetInsightsQuery(ecg_id, UserToken()))
        # then
        assert result == Insights(
            ecg_id,
            leads=[
                Insight('I', 3),
                Insight('II', 0)
            ]
        )
