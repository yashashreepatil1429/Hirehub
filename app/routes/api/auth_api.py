from flask import Blueprint, jsonify, request

from app.exceptions import InvalidCredentialsError, UserAlreadyExistsError
from app.services.auth_service import AuthService


auth_api_bp = Blueprint('auth_api', __name__, url_prefix='/api/auth')


@auth_api_bp.route('/register', methods=['POST'])
def register():
    try:
        user = AuthService().register(request.get_json(silent=True) or {})
        return jsonify({'success': True, 'message': 'Registration successful', 'data': user}), 201
    except (UserAlreadyExistsError, ValueError) as exc:
        return jsonify({'success': False, 'message': str(exc), 'error_code': 'REGISTRATION_FAILED'}), 400


@auth_api_bp.route('/login', methods=['POST'])
def login():
    payload = request.get_json(silent=True) or {}
    try:
        user = AuthService().login(payload.get('email', ''), payload.get('password', ''))
        return jsonify({'success': True, 'message': 'Login successful', 'data': user})
    except InvalidCredentialsError as exc:
        return jsonify({'success': False, 'message': str(exc), 'error_code': 'INVALID_CREDENTIALS'}), 401


@auth_api_bp.route('/logout', methods=['POST'])
def logout():
    AuthService().logout()
    return jsonify({'success': True, 'message': 'Logged out'})


@auth_api_bp.route('/me', methods=['GET'])
def me():
    user = AuthService().current_user()
    if not user:
        return jsonify({'success': False, 'message': 'Not authenticated', 'error_code': 'NOT_AUTHENTICATED'}), 401
    return jsonify({'success': True, 'data': user})
