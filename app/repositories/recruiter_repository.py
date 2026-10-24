from __future__ import annotations

from typing import Any, Dict, List, Optional

from app.repositories.base_repository import BaseRepository


class RecruiterRepository(BaseRepository):
    collection_name = 'recruiters'

    def create(self, recruiter: Dict[str, Any]) -> Dict[str, Any]:
        return self.insert(recruiter)

    def get_by_user_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        return self.find_one({'user_id': user_id})

    def get_by_id(self, recruiter_id: str) -> Optional[Dict[str, Any]]:
        return self.find_by_id(recruiter_id)

    def list_recruiters(self) -> List[Dict[str, Any]]:
        return self.find_all()
