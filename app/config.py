import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env')


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    MONGO_URI = os.getenv('MONGO_URI', '')
    MONGO_DATABASE = os.getenv('MONGO_DATABASE', 'hirehub')
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', str(BASE_DIR / 'uploads' / 'resumes'))
    MAX_CONTENT_LENGTH = int(os.getenv('MAX_CONTENT_LENGTH', 5 * 1024 * 1024))
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    SESSION_COOKIE_SECURE = False


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    SECRET_KEY = 'test-secret-key'
    MONGO_URI = ''


class ProductionConfig(Config):
    SESSION_COOKIE_SECURE = True
