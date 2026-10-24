from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict
import uuid


@dataclass
class Notification:
    user_id: str
    title: str
    message: str
    is_read: bool = False
    created_at: str = field(default_factory=lambda: __import__('datetime').datetime.utcnow().isoformat())
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Notification':
        return cls(**data)

    def to_dict(self) -> Dict[str, Any]:
        return self.__dict__.copy()
