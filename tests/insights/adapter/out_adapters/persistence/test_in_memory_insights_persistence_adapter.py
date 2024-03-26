from unittest.mock import patch

from freezegun import freeze_time

from src.ecg.domain.ecg import EcgId
from src.insights.adapter.out_adapters.persistence.in_memory_insights_persistence_adapter import \
    InMemoryInsightsPersistenceAdapter
from src.insights.domain.insights import Insights, Insight, InsightsId


class TestInMemoryInsightsPersistenceAdapter:
    _adapter: InMemoryInsightsPersistenceAdapter = InMemoryInsightsPersistenceAdapter({})

    @freeze_time()
    @patch('src.insights.domain.insights.uuid.uuid4', return_value="uuid4_generated_id")
    def test_it_saves_insights(self, mocker):
        # given
        insights = Insights(EcgId("id"), [Insight("I", 2)])
        # when
        result = self._adapter.save(insights)
        # then
        assert result == InsightsId("uuid4_generated_id")

    def test_it_returns_nothing_if_insights_not_found_by_ecg_id(self):
        # when
        result = self._adapter.get_by_ecg_id(EcgId("missing_ecg"))
        # then
        assert result is None

    @freeze_time()
    @patch('src.insights.domain.insights.uuid.uuid4', return_value="uuid4_generated_id")
    def test_it_retrieves_insights_by_ecg_id(self, mocker):
        # given
        insights = Insights(EcgId("id"), [Insight("I", 2)])
        self._adapter.save(insights)
        # when
        result = self._adapter.get_by_ecg_id(EcgId("id"))
        # then
        assert result == Insights(EcgId("id"), [Insight("I", 2)])
