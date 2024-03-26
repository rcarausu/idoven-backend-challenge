from abc import ABCMeta, abstractmethod

from src.user.domain.user import UserId, User


class SaveUserPort(metaclass=ABCMeta):

    @abstractmethod
    def save(self, user: User) -> UserId:
        raise NotImplementedError
