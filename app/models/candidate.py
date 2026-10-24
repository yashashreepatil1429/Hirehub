from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import uuid


@dataclass
class Candidate:
    user_id: str
    name: str
    email: str
    phone: str
    location: str = ''
    skills: List[str] = field(default_factory=list)
    education: str = ''
    experience: int = 0
    expected_salary: int = 0
    notice_period: str = ''
    resume: Optional[str] = None
    saved_jobs: List[str] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: __import__('datetime').datetime.utcnow().isoformat())
    updated_at: str = field(default_factory=lambda: __import__('datetime').datetime.utcnow().isoformat())
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Candidate':
        return cls(**data)

    def to_dict(self) -> Dict[str, Any]:
        return self.__dict__.copy()
