from __future__ import annotations

from typing import Any, Dict, List

from app.repositories.application_repository import ApplicationRepository
from app.repositories.analytics_repository import AnalyticsRepository
from app.repositories.job_repository import JobRepository
from app.repositories.user_repository import UserRepository


class AnalyticsService:
    def __init__(self, application_repository: ApplicationRepository | None = None, job_repository: JobRepository | None = None, user_repository: UserRepository | None = None):
        self.application_repository = application_repository or ApplicationRepository()
        self.job_repository = job_repository or JobRepository()
        self.user_repository = user_repository or UserRepository()
        self.analytics_repository = AnalyticsRepository()

    def dashboard_metrics(self) -> Dict[str, Any]:
        summary = self.analytics_repository.get_summary()
        jobs = self.job_repository.list_jobs()
        applications = self.application_repository.list_applications()
        return {
            'total_users': summary['users'],
            'total_jobs': summary['jobs'],
            'total_applications': summary['applications'],
            'open_jobs': sum(1 for job in jobs if str(job.get('status', '')).upper() == 'OPEN'),
            'shortlisted': sum(1 for app in applications if str(app.get('status', '')).upper() == 'SHORTLISTED'),
            'interviews': summary['interviews'],
        }

    def jobs_by_location(self) -> List[Dict[str, Any]]:
        return self.analytics_repository.aggregate_labels('jobs', 'location')

    def applications_by_status(self) -> List[Dict[str, Any]]:
        return self.analytics_repository.aggregate_labels('applications', 'status')
