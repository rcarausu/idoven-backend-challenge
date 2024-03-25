import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class UserId:
    value: str = field(default_factory=lambda: str(uuid.uuid4()))


@dataclass
class UserToken:
    value: str = field(default_factory=lambda: str(uuid.uuid4()))


@dataclass
class User:
    username: str
    id: UserId = field(default_factory=lambda: UserId())
    token: UserToken = field(default_factory=lambda: UserToken())
    create_date: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

