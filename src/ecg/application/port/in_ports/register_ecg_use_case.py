from abc import abstractmethod, ABCMeta
from dataclasses import dataclass
from typing import List

from src.ecg.domain.ecg import EcgId, Lead
from src.user.domain.user import UserToken


@dataclass
class RegisterEcgCommand:
    user_token: UserToken
    leads: List[Lead]


class RegisterEcgUseCase(metaclass=ABCMeta):

    @abstractmethod
    def register_ecg(self, command: RegisterEcgCommand) -> EcgId:
        pass
