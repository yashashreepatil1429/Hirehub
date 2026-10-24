from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, Optional
import uuid


@dataclass
class User:
    name: str
    email: str
    phone: str
    password_hash: str
    role: str = 'CANDIDATE'
    is_active: bool = True
    created_at: str = field(default_factory=lambda: __import__('datetime').datetime.utcnow().isoformat())
    updated_at: str = field(default_factory=lambda: __import__('datetime').datetime.utcnow().isoformat())
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'User':
        return cls(**data)

    def to_dict(self) -> Dict[str, Any]:
        data = self.__dict__.copy()
        data.pop('password_hash', None)
        return data

    @property
    def is_admin(self) -> bool:
        return self.role == 'ADMIN'

    @staticmethod
    def normalize_role(role: Optional[str]) -> str:
        return (role or 'CANDIDATE').upper()
