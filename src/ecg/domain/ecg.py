import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import List, Optional


@dataclass
class Lead:
    name: str
    signal: List[int]
    number_of_samples: Optional[int] = field(default=None)

    def number_of_zero_crossings(self):
        crossings = 0
        if len(self.signal) in (0, 1):
            return crossings
        previous_value = self.signal[0]
        for value in self.signal[1::]:
            if value == 0:
                if previous_value != 0:
                    crossings += 1
            elif value * previous_value < 0:
                crossings += 1
            previous_value = value
        return crossings


@dataclass
class ECG:
    ecg_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    create_date: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    leads: List[Lead] = field(default_factory=lambda: [])
