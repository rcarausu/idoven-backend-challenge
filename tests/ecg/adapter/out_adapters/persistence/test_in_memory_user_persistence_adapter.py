from unittest.mock import patch

from freezegun import freeze_time

from src.ecg.domain.user import User, UserId
from src.ecg.adapter.out_adapters.persistence.in_memory_user_persistence_adapter import InMemoryUserPersistenceAdapter
from src.ecg.domain.ecg import ECG, EcgId, Lead


class TestInMemoryEcgPersistenceAdapter:

    _adapter = InMemoryUserPersistenceAdapter()

    def test_it_saves_an_user(self):
        # given
        user = User("username", UserId("id"))
        # when
        result = self._adapter.save(user)
        # then
        assert isinstance(result, UserId)
        assert result.value == "id"
        assert user.username == "username"

    @freeze_time()
    @patch('src.ecg.domain.user.uuid.uuid4', return_value="uuid4_generated_id")
    def test_it_retrieves_an_user(self, mocker):
        # given
        user = User("username")
        self._adapter.save(user)
        # when
        result = self._adapter.get(UserId("uuid4_generated_id"))
        # then
        assert result == User("username")
