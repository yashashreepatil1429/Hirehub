from __future__ import annotations

from typing import Any, Dict, List, Optional

from app.repositories.base_repository import BaseRepository


class CandidateRepository(BaseRepository):
    collection_name = 'candidates'

    def create(self, candidate: Dict[str, Any]) -> Dict[str, Any]:
        return self.insert(candidate)

    def get_by_user_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        return self.find_one({'user_id': user_id})

    def get_by_id(self, candidate_id: str) -> Optional[Dict[str, Any]]:
        return self.find_by_id(candidate_id)

    def list_candidates(self) -> List[Dict[str, Any]]:
        return self.find_all()
