from flask import Flask

from app.config import DevelopmentConfig
from app.demo_accounts import seed_demo_accounts
from app.extensions import db
from app.routes.api import api_blueprints
from app.routes.web import web_blueprints


def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__, template_folder='templates', static_folder='static')
    app.config.from_object(config_class)
    db.init_app(app)
    if app.config.get('TESTING'):
        app.config.setdefault('DATA_STORE', {})
    with app.app_context():
        seed_demo_accounts()

    for blueprint in web_blueprints:
        app.register_blueprint(blueprint)
    for blueprint in api_blueprints:
        app.register_blueprint(blueprint)

    @app.route('/health')
    def health():
        return {'status': 'ok'}, 200

    @app.errorhandler(404)
    def page_not_found(error):
        return {'success': False, 'message': 'Resource not found', 'error_code': 'NOT_FOUND'}, 404

    return app
