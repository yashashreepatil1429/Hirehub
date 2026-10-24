from __future__ import annotations

from flask import current_app
from pymongo import ASCENDING, MongoClient


COLLECTIONS = (
    'users',
    'candidates',
    'recruiters',
    'companies',
    'jobs',
    'applications',
    'interviews',
    'resumes',
    'notifications',
    'audit_logs',
)

INDEXES = {
    'users': (([('email', ASCENDING)], {'unique': True}),),
    'jobs': (
        ([('title', ASCENDING)], {}),
        ([('skills', ASCENDING)], {}),
        ([('location', ASCENDING)], {}),
    ),
    'applications': (
        ([('candidate_id', ASCENDING)], {}),
        ([('job_id', ASCENDING)], {}),
        ([('candidate_id', ASCENDING), ('job_id', ASCENDING)], {'unique': True}),
    ),
}


class Database:
    def __init__(self):
        self.client = None
        self.database = None

    def init_app(self, app):
        mongo_uri = app.config.get('MONGO_URI')
        if app.config.get('TESTING'):
            app.config['USE_MOCK_DB'] = True
            app.config.setdefault('DATA_STORE', {})
            app.extensions['hirehub_mongo_client'] = None
            app.extensions['hirehub_mongo_database'] = None
            return
        if not mongo_uri:
            raise RuntimeError(
                'MONGO_URI is required. Configure MongoDB in the project-root .env file.'
            )

        client = MongoClient(
            mongo_uri,
            serverSelectionTimeoutMS=app.config.get('MONGO_SERVER_SELECTION_TIMEOUT_MS', 5000),
        )
        database = client[app.config.get('MONGO_DATABASE', 'hirehub')]
        app.extensions['hirehub_mongo_client'] = client
        app.extensions['hirehub_mongo_database'] = database
        self.client = client
        self.database = database
        database.command('ping')
        self._initialize_collections(database)
        self._initialize_indexes(database)
        app.config['USE_MOCK_DB'] = False

    @staticmethod
    def _initialize_collections(database):
        existing = set(database.list_collection_names())
        for name in COLLECTIONS:
            if name not in existing:
                database.create_collection(name)

    @staticmethod
    def _initialize_indexes(database):
        for collection_name, indexes in INDEXES.items():
            collection = database[collection_name]
            for keys, options in indexes:
                collection.create_index(keys, **options)

    def get_db(self, app=None):
        app = app or current_app
        if app.config.get('USE_MOCK_DB'):
            return app.config.setdefault('DATA_STORE', {})
        database = app.extensions.get('hirehub_mongo_database')
        if database is None:
            raise RuntimeError('MongoDB is not initialized for this application.')
        return database


db = Database()
