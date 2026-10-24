from __future__ import annotations

from typing import Any, Dict, List, Optional

from app.repositories.base_repository import BaseRepository


class ApplicationRepository(BaseRepository):
    collection_name = 'applications'

    def create(self, application: Dict[str, Any]) -> Dict[str, Any]:
        return self.insert(application)

    def get_by_id(self, application_id: str) -> Optional[Dict[str, Any]]:
        return self.find_by_id(application_id)

    def list_applications(self) -> List[Dict[str, Any]]:
        return self.find_all()

    def get_by_candidate_and_job(self, candidate_id: str, job_id: str) -> Optional[Dict[str, Any]]:
        return self.find_one({'candidate_id': candidate_id, 'job_id': job_id})

    def update_application(self, application_id: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        return self.update(application_id, data)
