from __future__ import annotations

from typing import Any

from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService


DEMO_ACCOUNTS = (
    {
        'name': 'HireHub Admin',
        'email': 'admin@hirehub.com',
        'phone': '9999999999',
        'password': 'Admin@123',
        'role': 'ADMIN',
    },
    {
        'name': 'Demo Recruiter',
        'email': 'recruiter@hirehub.com',
        'phone': '9999999998',
        'password': 'Recruiter@123',
        'role': 'RECRUITER',
    },
    {
        'name': 'Demo Candidate',
        'email': 'candidate@hirehub.com',
        'phone': '9999999997',
        'password': 'Candidate@123',
        'role': 'CANDIDATE',
    },
)


def seed_demo_accounts() -> None:
    repository = UserRepository()
    for account in DEMO_ACCOUNTS:
        if repository.get_by_email(account['email']):
            continue
        repository.create(AuthService.create_user_document(account))
