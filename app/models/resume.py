from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict
import uuid


@dataclass
class Resume:
    candidate_id: str
    filename: str
    original_name: str
    content_type: str
    size: int
    path: str
    created_at: str = field(default_factory=lambda: __import__('datetime').datetime.utcnow().isoformat())
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Resume':
        return cls(**data)

    def to_dict(self) -> Dict[str, Any]:
        return self.__dict__.copy()
