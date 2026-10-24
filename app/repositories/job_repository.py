from __future__ import annotations

from typing import Any, Dict, List, Optional

from app.repositories.base_repository import BaseRepository


class JobRepository(BaseRepository):
    collection_name = 'jobs'

    def create(self, job: Dict[str, Any]) -> Dict[str, Any]:
        return self.insert(job)

    def get_by_id(self, job_id: str) -> Optional[Dict[str, Any]]:
        return self.find_by_id(job_id)

    def list_jobs(self) -> List[Dict[str, Any]]:
        return self.find_all()

    def update_job(self, job_id: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        return self.update(job_id, data)

    def delete(self, job_id: str) -> bool:
        return super().delete(job_id)
