from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List
import uuid


@dataclass
class Recruiter:
    user_id: str
    name: str
    email: str
    phone: str
    company_name: str = ''
    company_id: str = ''
    skills: List[str] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: __import__('datetime').datetime.utcnow().isoformat())
    updated_at: str = field(default_factory=lambda: __import__('datetime').datetime.utcnow().isoformat())
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Recruiter':
        return cls(**data)

    def to_dict(self) -> Dict[str, Any]:
        return self.__dict__.copy()
