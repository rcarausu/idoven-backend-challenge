from typing import Optional

from src.ecg.application.port.out_ports.get_user_port import GetUserPort
from src.ecg.application.port.out_ports.save_user_port import SaveUserPort
from src.ecg.domain.user import UserId, User


class InMemoryUserPersistenceAdapter(GetUserPort, SaveUserPort):

    def __init__(self):
        self.__repository = {}

    def get(self, user_id: UserId) -> Optional[User]:
        # O(1) retrieval for average case or O(n) in_adapters worst case (hash collisions or too high load factor)
        return self.__repository.get(user_id.value, None)

    def save(self, user: User) -> UserId:
        # O(1) insertion by using a dictionary
        self.__repository[user.id.value] = user
        return user.id
