from freezegun import freeze_time

from src.ecg.adapter.out_adapters.persistence.in_memory_ecg_persistence_adapter import InMemoryEcgPersistenceAdapter
from src.ecg.domain.ecg import ECG, EcgId, Lead
from src.user.domain.user import UserId


class TestInMemoryEcgPersistenceAdapter:
    _adapter = InMemoryEcgPersistenceAdapter({})

    def test_it_saves_an_ecg(self):
        # given
        ecg = ECG(id=EcgId("id"), user_id=UserId("id"))
        # when
        result = self._adapter.save(ecg)
        # then
        assert isinstance(result, EcgId)
        assert result.value == "id"

    @freeze_time()
    def test_it_retrieves_an_ecg(self):
        # given
        ecg = ECG(id=EcgId("id"), user_id=UserId("id"), leads=[Lead("V1", number_of_samples=3, signal=[-1, 0, 1])])
        self._adapter.save(ecg)
        # when
        result = self._adapter.get(EcgId("id"))
        # then
        assert result == ECG(id=EcgId("id"), user_id=UserId("id"), leads=[Lead("V1", number_of_samples=3, signal=[-1, 0, 1])])
