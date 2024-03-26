import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import List, Optional

from src.user.domain.user import UserId


@dataclass
class Lead:
    name: str
    signal: List[int]
    number_of_samples: Optional[int] = field(default=None)


@dataclass
class EcgId:
    value: str = field(default_factory=lambda: str(uuid.uuid4()))

    def __eq__(self, other):
        return self.value == other.value

    def __str__(self):
        return self.value


@dataclass
class ECG:
    user_id: UserId
    id: EcgId = field(default_factory=lambda: EcgId())
    create_date: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    leads: List[Lead] = field(default_factory=list)
