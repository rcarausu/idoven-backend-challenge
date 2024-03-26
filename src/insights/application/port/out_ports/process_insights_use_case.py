from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from typing import List

from src.ecg.domain.ecg import Lead, EcgId


@dataclass
class ProcessInsightsCommand:
    ecg_id: EcgId
    leads: List[Lead]


class ProcessInsightsUseCase(metaclass=ABCMeta):

    @abstractmethod
    def process_insights(self, command: ProcessInsightsCommand) -> bool:
        raise NotImplementedError()
