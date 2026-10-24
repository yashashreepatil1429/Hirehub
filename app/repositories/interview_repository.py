from __future__ import annotations

from typing import Any, Dict, List, Optional

from app.repositories.base_repository import BaseRepository


class InterviewRepository(BaseRepository):
    collection_name = 'interviews'

    def create(self, interview: Dict[str, Any]) -> Dict[str, Any]:
        return self.insert(interview)

    def list_interviews(self) -> List[Dict[str, Any]]:
        return self.find_all()

    def get_by_id(self, interview_id: str) -> Optional[Dict[str, Any]]:
        return self.find_by_id(interview_id)

    def update_interview(self, interview_id: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        return self.update(interview_id, data)
