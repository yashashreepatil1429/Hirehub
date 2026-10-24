from flask import Blueprint, jsonify

from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService

admin_api_bp = Blueprint('admin_api', __name__, url_prefix='/api/admin')


@admin_api_bp.route('/users')
def list_users():
    users = [AuthService.safe_user(user) for user in UserRepository().list_users()]
    return jsonify({'success': True, 'data': users})
