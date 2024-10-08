from unittest.mock import patch

from freezegun import freeze_time

from src.user.adapter.out_adapters.in_memory_user_persistence_adapter import InMemoryUserPersistenceAdapter
from src.user.domain.user import User, UserId, UserToken


class TestInMemoryEcgPersistenceAdapter:
    _adapter: InMemoryUserPersistenceAdapter

    def setup_method(self):
        self._adapter = InMemoryUserPersistenceAdapter({})

    def test_it_saves_an_user(self):
        # given
        user = User("username", UserId("id"))
        # when
        result = self._adapter.save(user)
        # then
        assert isinstance(result, UserId)
        assert result.value == "id"
        assert user.username == "username"

    def test_it_returns_nothing_if_user_not_found_by_token(self):
        # when
        result = self._adapter.get_by_token(UserToken())
        # then
        assert result is None

    @freeze_time()
    @patch('src.user.domain.user.uuid.uuid4', return_value="uuid4_generated_id")
    def test_it_retrieves_an_user_by_token(self, mocker):
        # given
        user = User("username")
        self._adapter.save(user)
        # when
        result = self._adapter.get_by_token(UserToken("uuid4_generated_id"))
        # then
        assert result == User("username")
