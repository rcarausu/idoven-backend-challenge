import pytest

from src.ecg.domain.insights import Insights, Insight


class TestInsights:

    def test_it_should_raise_value_error_if_number_of_zero_crossings_is_a_negative_integer(self):
        # given
        with pytest.raises(ValueError) as e:
            Insight('I', -1)
        # then
        assert e.value.args[0] == "number_of_zero_crossings cannot be negative"

    def test_it_creates_insights_successfully(self):
        # given
        insights = Insights([Insight('I', 10)])
        # then
        assert insights == Insights([Insight('I', 10)])
