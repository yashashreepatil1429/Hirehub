from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, Optional
from uuid import uuid4

from app.repositories.base_repository import BaseRepository


class AuditService:
    def __init__(self, repository: BaseRepository | None = None):
        self.repository = repository or BaseRepository()
        self.repository.collection_name = 'audit_logs'

    def record(
        self,
        action: str,
        user_id: Optional[str],
        resource: str,
        resource_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        entry = {
            'id': uuid4().hex,
            'user_id': user_id,
            'action': action,
            'resource': resource,
            'resource_id': resource_id,
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'metadata': metadata or {},
        }
        return self.repository.insert(entry)
