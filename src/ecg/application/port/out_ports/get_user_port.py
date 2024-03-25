from abc import ABCMeta, abstractmethod
from typing import Optional

from src.ecg.domain.user import User, UserId


class UserNotFoundError(Exception):
    def __init__(self, user_id: UserId):
        self.message = f"User not found for id {user_id.value}"
        super().__init__(self.message)


class GetUserPort(metaclass=ABCMeta):
    @abstractmethod
    def get(self, user_id: UserId) -> Optional[User]:
        raise NotImplementedError
