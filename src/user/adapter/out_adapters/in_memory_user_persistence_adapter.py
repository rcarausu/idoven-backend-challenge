from typing import Optional

from src.user.domain.user import UserToken
from src.user.application.port.out_ports.get_user_port import GetUserPort
from src.user.application.port.out_ports.save_user_port import SaveUserPort
from src.user.domain.user import UserId, User


class InMemoryUserPersistenceAdapter(GetUserPort, SaveUserPort):

    def __init__(self, repository: dict):
        self.__repository = repository

    def get_by_token(self, user_token: UserToken) -> Optional[User]:
        # O(n) retrieval time since we have to iterate through all keys in the worst case
        for user_id in self.__repository.keys():
            if self.__repository[user_id].token == user_token:
                return self.__repository[user_id]
        return None

    def save(self, user: User) -> UserId:
        # O(n) insertion since we need to iterate to find any possible duplicates and overwrite them, since
        #  users should be unique per username
        for user_id in self.__repository.keys():
            current_user: User = self.__repository[user_id]
            if self.__repository[user_id].username == user.username:
                updated_user = User(
                    id=current_user.id,
                    username=current_user.username,
                    token=user.token,
                    create_date=current_user.create_date
                )
                self.__repository[user_id] = updated_user
                return updated_user.id
        self.__repository[user.id.value] = user
        return user.id
