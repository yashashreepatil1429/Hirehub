from __future__ import annotations

from typing import Any, Dict, List, Optional

from app.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository):
    collection_name = 'users'

    def create(self, user: Dict[str, Any]) -> Dict[str, Any]:
        return self.insert(user)

    def get_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        return self.find_one({'email': email})

    def get_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        return self.find_by_id(user_id)

    def list_users(self) -> List[Dict[str, Any]]:
        return self.find_all()

    def update_user(self, user_id: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        return self.update(user_id, data)
