from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List

from app.repositories.base_repository import BaseRepository


class NotificationService:
    def __init__(self, repository: BaseRepository | None = None):
        self.repository = repository or BaseRepository()
        self.repository.collection_name = 'notifications'

    def create(self, user_id: str, title: str, message: str) -> Dict[str, Any]:
        notification = {
            'id': __import__('uuid').uuid4().hex,
            'user_id': user_id,
            'title': title,
            'message': message,
            'is_read': False,
            'created_at': datetime.utcnow().isoformat(),
        }
        self.repository.insert(notification)
        return notification

    def list_for_user(self, user_id: str) -> List[Dict[str, Any]]:
        return [n for n in self.repository.find_all() if n.get('user_id') == user_id]

    def mark_read(self, notification_id: str) -> Dict[str, Any] | None:
        notification = self.repository.find_by_id(notification_id)
        if not notification:
            return None
        notification['is_read'] = True
        self.repository.update(notification_id, notification)
        return notification
