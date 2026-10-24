from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional

from app.repositories.application_repository import ApplicationRepository
from app.repositories.candidate_repository import CandidateRepository
from app.repositories.interview_repository import InterviewRepository
from app.repositories.job_repository import JobRepository


class CandidateService:
    def __init__(self, candidate_repository: CandidateRepository | None = None):
        self.candidate_repository = candidate_repository or CandidateRepository()
        self.job_repository = JobRepository()
        self.application_repository = ApplicationRepository()
        self.interview_repository = InterviewRepository()

    def profile(self, user_id: str) -> Optional[Dict[str, Any]]:
        return self.candidate_repository.get_by_user_id(user_id)

    def save_profile(self, user_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        candidate = self.candidate_repository.get_by_user_id(user_id)
        is_new = candidate is None
        if candidate is None:
            candidate = {'user_id': user_id, 'id': __import__('uuid').uuid4().hex}
        candidate.update({
            'user_id': user_id,
            'name': data.get('name', candidate.get('name', '')),
            'email': data.get('email', candidate.get('email', '')),
            'phone': data.get('phone', candidate.get('phone', '')),
            'location': data.get('location', candidate.get('location', '')),
            'skills': data.get('skills', candidate.get('skills', [])),
            'education': data.get('education', candidate.get('education', '')),
            'experience': data.get('experience', candidate.get('experience', 0)),
            'expected_salary': data.get('expected_salary', candidate.get('expected_salary', 0)),
            'notice_period': data.get('notice_period', candidate.get('notice_period', '')),
            'resume': data.get('resume', candidate.get('resume')),
            'saved_jobs': candidate.get('saved_jobs', []),
            'updated_at': datetime.utcnow().isoformat(),
        })
        if is_new:
            self.candidate_repository.create(candidate)
        else:
            self.candidate_repository.update(candidate['id'], candidate)
        return candidate

    def get_applications(self, candidate_id: str) -> List[Dict[str, Any]]:
        return [app for app in self.application_repository.list_applications() if app.get('candidate_id') == candidate_id]

    def get_interviews(self, candidate_id: str) -> List[Dict[str, Any]]:
        return [item for item in self.interview_repository.list_interviews() if item.get('candidate_id') == candidate_id]

    def save_job(self, candidate_id: str, job_id: str) -> Dict[str, Any]:
        candidate = self.candidate_repository.get_by_id(candidate_id) or self.candidate_repository.get_by_user_id(candidate_id)
        if not candidate:
            raise ValueError('Candidate not found')
        saved = candidate.setdefault('saved_jobs', [])
        if job_id not in saved:
            saved.append(job_id)
        candidate['updated_at'] = datetime.utcnow().isoformat()
        self.candidate_repository.update(candidate['id'], candidate)
        return candidate
