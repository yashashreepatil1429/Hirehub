from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List

from app.repositories.application_repository import ApplicationRepository
from app.repositories.company_repository import CompanyRepository
from app.repositories.interview_repository import InterviewRepository
from app.repositories.job_repository import JobRepository


class RecruiterService:
    def __init__(self, company_repository: CompanyRepository | None = None):
        self.company_repository = company_repository or CompanyRepository()
        self.job_repository = JobRepository()
        self.application_repository = ApplicationRepository()
        self.interview_repository = InterviewRepository()

    def create_company(self, data: Dict[str, Any]) -> Dict[str, Any]:
        company = {
            'id': data.get('id') or __import__('uuid').uuid4().hex,
            'name': data.get('name', ''),
            'company_type': data.get('company_type', 'IT'),
            'location': data.get('location', ''),
            'website': data.get('website', ''),
            'description': data.get('description', ''),
            'verified': data.get('verified', False),
            'recruiter_id': data.get('recruiter_id', ''),
            'created_at': datetime.utcnow().isoformat(),
            'updated_at': datetime.utcnow().isoformat(),
        }
        self.company_repository.create(company)
        return company

    def create_job(self, recruiter_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        job = {
            'id': data.get('id') or __import__('uuid').uuid4().hex,
            'company_id': data.get('company_id', ''),
            'recruiter_id': recruiter_id,
            'title': data.get('title', ''),
            'description': data.get('description', ''),
            'skills': data.get('skills', []),
            'experience_min': data.get('experience_min', 0),
            'experience_max': data.get('experience_max', 0),
            'location': data.get('location', ''),
            'work_mode': data.get('work_mode', 'REMOTE').upper(),
            'employment_type': data.get('employment_type', 'FULL_TIME').upper(),
            'salary_min': data.get('salary_min', 0),
            'salary_max': data.get('salary_max', 0),
            'posted_date': data.get('posted_date') or datetime.utcnow().date().isoformat(),
            'deadline': data.get('deadline') or datetime.utcnow().date().isoformat(),
            'status': data.get('status', 'OPEN'),
            'created_at': datetime.utcnow().isoformat(),
            'updated_at': datetime.utcnow().isoformat(),
        }
        self.job_repository.create(job)
        return job

    def get_applications_for_jobs(self, recruiter_id: str) -> List[Dict[str, Any]]:
        jobs = [job for job in self.job_repository.list_jobs() if job.get('recruiter_id') == recruiter_id]
        job_ids = {job['id'] for job in jobs}
        return [app for app in self.application_repository.list_applications() if app.get('job_id') in job_ids]

    def shortlist_application(self, application_id: str) -> Dict[str, Any]:
        app = self.application_repository.get_by_id(application_id)
        if not app:
            raise ValueError('Application not found')
        app['status'] = 'SHORTLISTED'
        app['updated_at'] = datetime.utcnow().isoformat()
        self.application_repository.update_application(application_id, app)
        return app

    def reject_application(self, application_id: str) -> Dict[str, Any]:
        app = self.application_repository.get_by_id(application_id)
        if not app:
            raise ValueError('Application not found')
        app['status'] = 'REJECTED'
        app['updated_at'] = datetime.utcnow().isoformat()
        self.application_repository.update_application(application_id, app)
        return app
