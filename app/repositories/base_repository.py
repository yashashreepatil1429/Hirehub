from __future__ import annotations

from typing import Any, Dict, List, Optional

from flask import current_app
from pymongo import ASCENDING
from pymongo.collection import Collection


class BaseRepository:
    collection_name = 'items'

    def _collection(self) -> Collection | None:
        database = current_app.extensions.get('hirehub_mongo_database')
        if database is None:
            if not current_app.config.get('TESTING'):
                raise RuntimeError('MongoDB is not initialized for this application.')
            return None
        return database[self.collection_name]

    def _store(self) -> Dict[str, Dict[str, Any]]:
        data_store = current_app.config.setdefault('DATA_STORE', {})
        return data_store.setdefault(self.collection_name, {})

    @staticmethod
    def _serialize(document: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        if document is None:
            return None
        document.pop('_id', None)
        return document

    def insert(self, item: Dict[str, Any]) -> Dict[str, Any]:
        item_id = item.get('id') or item.get('_id')
        if not item_id:
            raise ValueError('Item must have an id')
        collection = self._collection()
        if collection is not None:
            document = dict(item)
            document['id'] = str(item_id)
            collection.insert_one(document)
            return item
        self._store()[item_id] = item
        return item

    def find_all(self, filters: Optional[Dict[str, Any]] = None, sort_by: Optional[str] = None) -> List[Dict[str, Any]]:
        collection = self._collection()
        if collection is not None:
            cursor = collection.find(filters or {})
            if sort_by:
                cursor = cursor.sort(sort_by, ASCENDING)
            return [self._serialize(item) for item in cursor]
        items = list(self._store().values())
        if filters:
            items = [item for item in items if all(item.get(k) == v for k, v in filters.items())]
        if sort_by:
            items = sorted(items, key=lambda item: item.get(sort_by, ''))
        return items

    def find_one(self, filters: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        if not filters:
            return None
        collection = self._collection()
        if collection is not None:
            return self._serialize(collection.find_one(filters))
        for item in self._store().values():
            if all(item.get(k) == v for k, v in filters.items()):
                return item
        return None

    def find_by_id(self, item_id: str) -> Optional[Dict[str, Any]]:
        collection = self._collection()
        if collection is not None:
            return self._serialize(collection.find_one({'id': str(item_id)}))
        return self._store().get(item_id)

    def update(self, item_id: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        collection = self._collection()
        if collection is not None:
            updated = collection.find_one_and_update(
                {'id': str(item_id)},
                {'$set': data},
                return_document=True,
            )
            return self._serialize(updated)
        item = self._store().get(item_id)
        if not item:
            return None
        item.update(data)
        self._store()[item_id] = item
        return item

    def delete(self, item_id: str) -> bool:
        collection = self._collection()
        if collection is not None:
            return collection.delete_one({'id': str(item_id)}).deleted_count > 0
        return self._store().pop(item_id, None) is not None

    def count(self, filters: Optional[Dict[str, Any]] = None) -> int:
        collection = self._collection()
        if collection is not None:
            return collection.count_documents(filters or {})
        return len(self.find_all(filters))

    def exists(self, filters: Optional[Dict[str, Any]] = None) -> bool:
        return self.find_one(filters) is not None

    def paginate(
        self,
        filters: Optional[Dict[str, Any]] = None,
        page: int = 1,
        per_page: int = 20,
        sort_by: str = 'created_at',
    ) -> tuple[List[Dict[str, Any]], int]:
        page = max(1, page)
        per_page = max(1, min(per_page, 100))
        collection = self._collection()
        if collection is not None:
            query = filters or {}
            total = collection.count_documents(query)
            cursor = (
                collection.find(query)
                .sort(sort_by, ASCENDING)
                .skip((page - 1) * per_page)
                .limit(per_page)
            )
            return [self._serialize(item) for item in cursor], total
        items = self.find_all(filters, sort_by)
        start = (page - 1) * per_page
        return items[start:start + per_page], len(items)
