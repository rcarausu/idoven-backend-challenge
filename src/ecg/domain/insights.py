from dataclasses import dataclass
from typing import List


@dataclass
class Insight:
    name: str
    number_of_zero_crossings: int = 0

    def __post_init__(self):
        if self.number_of_zero_crossings < 0:
            raise ValueError("number_of_zero_crossings cannot be negative")


@dataclass
class Insights:
    leads: List[Insight]
