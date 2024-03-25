from unittest.mock import patch

from freezegun import freeze_time

from src.ecg.adapter.out_adapters.persistence.in_memory_user_persistence_adapter import InMemoryUserPersistenceAdapter
from src.ecg.domain.user import User, UserId, UserToken


class TestInMemoryEcgPersistenceAdapter:
    _adapter: InMemoryUserPersistenceAdapter = InMemoryUserPersistenceAdapter()

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
        result = self._adapter.get_by_id(UserId("uuid4_generated_id"))
        # then
        assert result == User("username")

    def test_it_returns_nothing_if_user_not_found_by_id(self):
        # when
        result = self._adapter.get_by_id(UserId())
        # then
        assert result is None

    def test_it_returns_nothing_if_user_not_found_by_token(self):
        # when
        result = self._adapter.get_by_token(UserToken())
        # then
        assert result is None

    @freeze_time()
    @patch('src.ecg.domain.user.uuid.uuid4', return_value="uuid4_generated_id")
    def test_it_retrieves_an_user_by_token(self, mocker):
        # given
        user = User("username")
        self._adapter.save(user)
        # when
        result = self._adapter.get_by_token(UserToken("uuid4_generated_id"))
        # then
        assert result == User("username")
