from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, Optional

from flask import session
from werkzeug.security import check_password_hash, generate_password_hash

from app.exceptions import InvalidCredentialsError, UserAlreadyExistsError
from app.repositories.user_repository import UserRepository
from app.services.audit_service import AuditService
from app.utils.validators import is_valid_email, is_valid_password, is_valid_phone


class AuthService:
    def __init__(self, user_repository: UserRepository | None = None):
        self.user_repository = user_repository or UserRepository()

    @staticmethod
    def create_user_document(data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            'id': data.get('id') or data.get('_id') or __import__('uuid').uuid4().hex,
            'name': data['name'],
            'email': data['email'].lower(),
            'phone': data.get('phone', ''),
            'password_hash': generate_password_hash(data['password']),
            'role': data.get('role', 'CANDIDATE').upper(),
            'is_active': True,
            'created_at': datetime.utcnow().isoformat(),
            'updated_at': datetime.utcnow().isoformat(),
        }

    def register(self, data: Dict[str, Any]) -> Dict[str, Any]:
        email = (data.get('email') or '').strip().lower()
        password = data.get('password') or ''
        role = (data.get('role') or 'CANDIDATE').strip().upper()
        if role not in {'CANDIDATE', 'RECRUITER'}:
            raise ValueError('Only candidate and recruiter accounts can be registered')
        if not is_valid_email(email):
            raise ValueError('Invalid email')
        if not is_valid_password(password):
            raise ValueError('Password must be at least 6 characters')
        if self.user_repository.get_by_email(email):
            raise UserAlreadyExistsError()
        user = self.create_user_document(data)
        user['email'] = email
        user['role'] = role
        if not is_valid_phone(user.get('phone', '')):
            raise ValueError('Invalid phone number')
        self.user_repository.create(user)
        session['user_id'] = user['id']
        session['role'] = user['role']
        AuditService().record('USER_REGISTERED', user['id'], 'user', user['id'], {'role': user['role']})
        return self.safe_user(user)

    def login(self, email: str, password: str) -> Dict[str, Any]:
        email = (email or '').strip().lower()
        user = self.user_repository.get_by_email(email)
        if not user or not check_password_hash(user.get('password_hash', ''), password):
            raise InvalidCredentialsError()
        if not user.get('is_active', True):
            raise InvalidCredentialsError('Account is inactive')
        session['user_id'] = user['id']
        session['role'] = user['role']
        AuditService().record('USER_LOGIN', user['id'], 'user', user['id'])
        return self.safe_user(user)

    def logout(self) -> None:
        user_id = session.get('user_id')
        if user_id:
            AuditService().record('USER_LOGOUT', user_id, 'user', user_id)
        session.clear()

    @staticmethod
    def safe_user(user: Dict[str, Any]) -> Dict[str, Any]:
        safe = dict(user)
        safe.pop('password_hash', None)
        return safe

    def get_user(self, user_id: str) -> Optional[Dict[str, Any]]:
        user = self.user_repository.get_by_id(user_id)
        return self.safe_user(user) if user else None

    @staticmethod
    def current_user() -> Dict[str, Any] | None:
        user_id = session.get('user_id')
        if not user_id:
            return None
        repo = UserRepository()
        return repo.get_by_id(user_id)
