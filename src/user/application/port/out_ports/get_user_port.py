from abc import ABCMeta, abstractmethod
from typing import Optional

from src.user.domain.user import User, UserId, UserToken


class UserNotFoundError(Exception):
    def __init__(self, user_id: UserId):
        self.message = f"User not found for id {user_id.value}"
        super().__init__(self.message)


class GetUserPort(metaclass=ABCMeta):

    @abstractmethod
    def get_by_token(self, user_token: UserToken) -> Optional[User]:
        raise NotImplementedError
