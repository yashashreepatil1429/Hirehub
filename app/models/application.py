from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, Optional
import uuid


@dataclass
class Application:
    candidate_id: str
    job_id: str
    status: str = 'APPLIED'
    applied_at: str = field(default_factory=lambda: __import__('datetime').datetime.utcnow().isoformat())
    updated_at: str = field(default_factory=lambda: __import__('datetime').datetime.utcnow().isoformat())
    recruiter_notes: str = ''
    interview_id: Optional[str] = None
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Application':
        return cls(**data)

    def to_dict(self) -> Dict[str, Any]:
        return self.__dict__.copy()
