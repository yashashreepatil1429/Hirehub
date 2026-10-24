from flask import Blueprint, jsonify, request

from app.services.recruiter_service import RecruiterService

recruiter_api_bp = Blueprint('recruiter_api', __name__, url_prefix='/api/recruiters')


@recruiter_api_bp.route('/companies', methods=['POST'])
def create_company():
    data = request.get_json(silent=True) or {}
    company = RecruiterService().create_company(data)
    return jsonify({'success': True, 'message': 'Company created', 'data': company}), 201


@recruiter_api_bp.route('/jobs', methods=['POST'])
def create_job():
    data = request.get_json(silent=True) or {}
    job = RecruiterService().create_job(data.get('recruiter_id', 'demo'), data)
    return jsonify({'success': True, 'message': 'Job created', 'data': job}), 201
