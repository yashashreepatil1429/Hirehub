from __future__ import annotations

from app import create_app


def seed():
    create_app()

if __name__ == '__main__':
    seed()
    print('Initialized default demo accounts.')
