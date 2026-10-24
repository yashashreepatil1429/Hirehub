from __future__ import annotations

from typing import Any, Dict, List

from flask import current_app
from app.repositories.base_repository import BaseRepository


class AnalyticsRepository(BaseRepository):
    collection_name = 'jobs'

    def get_summary(self) -> Dict[str, Any]:
        database = current_app.extensions.get('hirehub_mongo_database')
        if database is None:
            if not current_app.config.get('TESTING'):
                raise RuntimeError('MongoDB is not initialized for this application.')
            return {
                'jobs': self.count(),
                'applications': len(current_app.config['DATA_STORE'].get('applications', {})),
                'users': len(current_app.config['DATA_STORE'].get('users', {})),
                'companies': len(current_app.config['DATA_STORE'].get('companies', {})),
                'interviews': len(current_app.config['DATA_STORE'].get('interviews', {})),
            }
        return {
            'jobs': database['jobs'].count_documents({}),
            'applications': database['applications'].count_documents({}),
            'users': database['users'].count_documents({}),
            'companies': database['companies'].count_documents({}),
            'interviews': database['interviews'].count_documents({}),
        }

    def list_stats(self) -> List[Dict[str, Any]]:
        database = current_app.extensions.get('hirehub_mongo_database')
        if database is None:
            if not current_app.config.get('TESTING'):
                raise RuntimeError('MongoDB is not initialized for this application.')
            return self.find_all()
        return list(database['jobs'].aggregate([
            {'$unwind': {'path': '$skills', 'preserveNullAndEmptyArrays': False}},
            {'$group': {'_id': '$skills', 'count': {'$sum': 1}}},
            {'$sort': {'count': -1, '_id': 1}},
        ]))

    @staticmethod
    def aggregate_labels(collection_name: str, field: str) -> List[Dict[str, Any]]:
        database = current_app.extensions.get('hirehub_mongo_database')
        if database is None:
            if not current_app.config.get('TESTING'):
                raise RuntimeError('MongoDB is not initialized for this application.')
            store = current_app.config['DATA_STORE'].get(collection_name, {})
            counts: Dict[str, int] = {}
            for document in store.values():
                label = str(document.get(field, 'Unknown'))
                counts[label] = counts.get(label, 0) + 1
            return [{'label': label, 'value': count} for label, count in sorted(counts.items())]
        return [
            {'label': item['_id'], 'value': item['count']}
            for item in database[collection_name].aggregate([
                {'$group': {'_id': {'$ifNull': [f'${field}', 'Unknown']}, 'count': {'$sum': 1}}},
                {'$sort': {'_id': 1}},
            ])
        ]
