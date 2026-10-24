from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import uuid


@dataclass
class Job:
    company_id: str
    recruiter_id: str
    title: str
    description: str
    skills: List[str]
    experience_min: int
    experience_max: int
    location: str
    work_mode: str
    employment_type: str
    salary_min: int
    salary_max: int
    posted_date: str
    deadline: str
    status: str = 'OPEN'
    created_at: str = field(default_factory=lambda: __import__('datetime').datetime.utcnow().isoformat())
    updated_at: str = field(default_factory=lambda: __import__('datetime').datetime.utcnow().isoformat())
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Job':
        return cls(**data)

    def to_dict(self) -> Dict[str, Any]:
        return self.__dict__.copy()
