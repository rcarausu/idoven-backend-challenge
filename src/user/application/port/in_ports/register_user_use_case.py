from abc import abstractmethod, ABCMeta
from dataclasses import dataclass

from src.user.domain.user import User, UserId


@dataclass
class AdminToken:
    value: str

    def __eq__(self, other):
        return self.value == other.value


@dataclass
class RegisterUserCommand:
    admin_token: AdminToken
    user: User


class RegisterUserUseCase(metaclass=ABCMeta):

    @abstractmethod
    def register_user(self, command: RegisterUserCommand) -> UserId:
        pass
