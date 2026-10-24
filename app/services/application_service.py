from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List

from app.exceptions import DuplicateApplicationError, InvalidApplicationStatusError, JobClosedError
from app.repositories.application_repository import ApplicationRepository
from app.repositories.job_repository import JobRepository
from app.services.audit_service import AuditService
from app.services.notification_service import NotificationService


class ApplicationService:
    def __init__(self, application_repository: ApplicationRepository | None = None):
        self.application_repository = application_repository or ApplicationRepository()
        self.job_repository = JobRepository()

    def apply(self, candidate_id: str, job_id: str) -> Dict[str, Any]:
        job = self.job_repository.get_by_id(job_id)
        if not job:
            raise ValueError('Job not found')
        if job.get('status') == 'CLOSED':
            raise JobClosedError()
        if job.get('deadline') and job['deadline'] < datetime.utcnow().date().isoformat():
            raise JobClosedError('Application deadline has passed')
        if self.application_repository.get_by_candidate_and_job(candidate_id, job_id):
            raise DuplicateApplicationError()
        application = {
            'id': __import__('uuid').uuid4().hex,
            'candidate_id': candidate_id,
            'job_id': job_id,
            'status': 'APPLIED',
            'applied_at': datetime.utcnow().isoformat(),
            'updated_at': datetime.utcnow().isoformat(),
            'recruiter_notes': '',
            'interview_id': None,
        }
        self.application_repository.create(application)
        NotificationService().create(
            candidate_id,
            'Application submitted',
            f'Your application for {job.get("title", "the job")} was submitted.',
        )
        AuditService().record('APPLICATION_SUBMITTED', candidate_id, 'application', application['id'])
        return application

    def list_for_candidate(self, candidate_id: str) -> List[Dict[str, Any]]:
        return [app for app in self.application_repository.list_applications() if app.get('candidate_id') == candidate_id]

    def get_by_id(self, application_id: str) -> Dict[str, Any] | None:
        return self.application_repository.get_by_id(application_id)

    def update_status(self, application_id: str, status: str) -> Dict[str, Any]:
        application = self.application_repository.get_by_id(application_id)
        if not application:
            raise ValueError('Application not found')
        allowed = {'APPLIED', 'UNDER_REVIEW', 'SHORTLISTED', 'INTERVIEW_SCHEDULED', 'SELECTED', 'REJECTED', 'WITHDRAWN'}
        if status not in allowed:
            raise InvalidApplicationStatusError()
        application['status'] = status
        application['updated_at'] = datetime.utcnow().isoformat()
        self.application_repository.update_application(application_id, application)
        return application
