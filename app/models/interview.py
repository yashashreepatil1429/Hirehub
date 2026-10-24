from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, Optional
import uuid


@dataclass
class Interview:
    application_id: str
    candidate_id: str
    recruiter_id: str
    date: str
    time: str
    type: str = 'ONLINE'
    meeting_link: str = ''
    status: str = 'SCHEDULED'
    feedback: Optional[str] = None
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Interview':
        return cls(**data)

    def to_dict(self) -> Dict[str, Any]:
        return self.__dict__.copy()
