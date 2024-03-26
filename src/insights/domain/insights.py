import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import List

from src.ecg.domain.ecg import EcgId


@dataclass
class Insight:
    name: str
    number_of_zero_crossings: int = 0

    def __post_init__(self):
        if self.number_of_zero_crossings < 0:
            raise ValueError("number_of_zero_crossings cannot be negative")


@dataclass
class InsightsId:
    value: str = field(default_factory=lambda: uuid.uuid4())

    def __eq__(self, other):
        return self.value == other.value

    def __str__(self):
        return self.value


@dataclass
class Insights:
    ecg_id: EcgId()
    leads: List[Insight]
    id: InsightsId = field(default_factory=lambda: InsightsId())
    create_date: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
