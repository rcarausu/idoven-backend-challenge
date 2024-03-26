from unittest.mock import patch

import pytest
from freezegun import freeze_time

from src.ecg.domain.ecg import EcgId
from src.insights.domain.insights import Insights, Insight


class TestInsights:

    def test_it_should_raise_value_error_if_number_of_zero_crossings_is_a_negative_integer(self):
        # given
        with pytest.raises(ValueError) as e:
            Insight('I', -1)
        # then
        assert e.value.args[0] == "number_of_zero_crossings cannot be negative"

    @freeze_time()
    @patch('src.insights.domain.insights.uuid.uuid4', return_value="uuid4_generated_id")
    def test_it_creates_insights_successfully(self, mocker):
        # given
        insights = Insights(EcgId("id"), [Insight('I', 10)])
        # then
        assert insights == Insights(EcgId("id"), [Insight('I', 10)])
