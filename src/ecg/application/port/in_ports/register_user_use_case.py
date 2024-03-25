from abc import abstractmethod, ABCMeta
from dataclasses import dataclass

from src.ecg.domain.user import User, UserId


class InvalidAdminTokenError(Exception):

    def __init__(self):
        self.message = "Invalid admin token, cannot perform requested action"
        super().__init__(self.message)


@dataclass
class AdminToken:
    value: str


@dataclass
class RegisterUserCommand:
    admin_token: AdminToken
    user: User


class RegisterUserUseCase(metaclass=ABCMeta):

    @abstractmethod
    def register_user(self, command: RegisterUserCommand) -> UserId:
        pass
