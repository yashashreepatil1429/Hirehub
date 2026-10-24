from __future__ import annotations

from typing import Any, Dict, List

from app.repositories.interview_repository import InterviewRepository


class InterviewService:
    def __init__(self, interview_repository: InterviewRepository | None = None):
        self.interview_repository = interview_repository or InterviewRepository()

    def schedule(self, data: Dict[str, Any]) -> Dict[str, Any]:
        interview = {
            'id': data.get('id') or __import__('uuid').uuid4().hex,
            'application_id': data.get('application_id', ''),
            'candidate_id': data.get('candidate_id', ''),
            'recruiter_id': data.get('recruiter_id', ''),
            'date': data.get('date', ''),
            'time': data.get('time', ''),
            'type': data.get('type', 'ONLINE').upper(),
            'meeting_link': data.get('meeting_link', ''),
            'status': data.get('status', 'SCHEDULED'),
            'feedback': data.get('feedback'),
        }
        self.interview_repository.create(interview)
        return interview

    def list_for_candidate(self, candidate_id: str) -> List[Dict[str, Any]]:
        return [item for item in self.interview_repository.list_interviews() if item.get('candidate_id') == candidate_id]

    def list_for_recruiter(self, recruiter_id: str) -> List[Dict[str, Any]]:
        return [item for item in self.interview_repository.list_interviews() if item.get('recruiter_id') == recruiter_id]
