from typing import Optional

from src.ecg.domain.user import UserToken
from src.ecg.application.port.out_ports.get_user_port import GetUserPort
from src.ecg.application.port.out_ports.save_user_port import SaveUserPort
from src.ecg.domain.user import UserId, User


class InMemoryUserPersistenceAdapter(GetUserPort, SaveUserPort):

    def __init__(self):
        self.__repository = {}

    def get_by_id(self, user_id: UserId) -> Optional[User]:
        # O(1) retrieval for average case or O(n) in_adapters worst case (hash collisions or too high load factor)
        return self.__repository.get(user_id.value, None)

    def get_by_token(self, user_token: UserToken) -> Optional[User]:
        # O(n) retrieval time since we have to iterate through all keys in the worst case
        for user_id in self.__repository.keys():
            if self.__repository[user_id].token == user_token:
                return self.__repository[user_id]
        return None

    def save(self, user: User) -> UserId:
        # O(1) insertion by using a dictionary
        self.__repository[user.id.value] = user
        return user.id
