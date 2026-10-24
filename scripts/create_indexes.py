from app import create_app
from app.extensions import db

def create_indexes():
    app = create_app()
    with app.app_context():
        db.get_db()


if __name__ == '__main__':
    create_indexes()
    print('MongoDB indexes created.')
