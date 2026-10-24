from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List

from app.repositories.job_repository import JobRepository


class JobService:
    def __init__(self, job_repository: JobRepository | None = None):
        self.job_repository = job_repository or JobRepository()

    def list_jobs(self, filters: dict | None = None) -> List[Dict[str, Any]]:
        jobs = self.job_repository.list_jobs()
        filters = filters or {}
        for key, value in filters.items():
            if not value:
                continue
            jobs = [job for job in jobs if str(job.get(key, '')).lower() == str(value).lower()]
        return jobs

    def get_by_id(self, job_id: str) -> Dict[str, Any] | None:
        return self.job_repository.get_by_id(job_id)

    def create_job(self, job: Dict[str, Any]) -> Dict[str, Any]:
        job['id'] = job.get('id') or __import__('uuid').uuid4().hex
        job['status'] = job.get('status', 'OPEN')
        job['created_at'] = datetime.utcnow().isoformat()
        job['updated_at'] = datetime.utcnow().isoformat()
        self.job_repository.create(job)
        return job

    def update_job(self, job_id: str, data: Dict[str, Any]) -> Dict[str, Any] | None:
        job = self.job_repository.get_by_id(job_id)
        if not job:
            return None
        job.update(data)
        job['updated_at'] = datetime.utcnow().isoformat()
        self.job_repository.update_job(job_id, job)
        return job

    def close_job(self, job_id: str) -> Dict[str, Any] | None:
        job = self.job_repository.get_by_id(job_id)
        if not job:
            return None
        job['status'] = 'CLOSED'
        job['updated_at'] = datetime.utcnow().isoformat()
        self.job_repository.update_job(job_id, job)
        return job

    def search(self, keyword: str = '', skills: str = '', location: str = '', work_mode: str = '', employment_type: str = '', company: str = '') -> List[Dict[str, Any]]:
        jobs = self.job_repository.list_jobs()
        q = keyword.lower()
        skill_tokens = [s.strip().lower() for s in (skills or '').split(',') if s.strip()]
        if q:
            jobs = [job for job in jobs if q in (job.get('title', '') + ' ' + job.get('description', '')).lower()]
        if skill_tokens:
            jobs = [job for job in jobs if any(skill.lower() in [s.lower() for s in job.get('skills', [])] for skill in skill_tokens)]
        if location:
            jobs = [job for job in jobs if str(job.get('location', '')).lower() == location.lower()]
        if work_mode:
            jobs = [job for job in jobs if str(job.get('work_mode', '')).lower() == work_mode.lower()]
        if employment_type:
            jobs = [job for job in jobs if str(job.get('employment_type', '')).lower() == employment_type.lower()]
        if company:
            jobs = [job for job in jobs if str(job.get('company_id', '')).lower() == company.lower()]
        return jobs
