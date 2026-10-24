from flask import Blueprint, jsonify, request

from app.services.application_service import ApplicationService

application_api_bp = Blueprint('application_api', __name__, url_prefix='/api/applications')


@application_api_bp.route('', methods=['GET'])
def list_applications():
    return jsonify({'success': True, 'data': ApplicationService().application_repository.list_applications()})


@application_api_bp.route('/<application_id>', methods=['GET'])
def get_application(application_id):
    return jsonify({'success': True, 'data': ApplicationService().get_by_id(application_id)})


@application_api_bp.route('/<application_id>/status', methods=['PUT'])
def update_status(application_id):
    payload = request.get_json(silent=True) or {}
    application = ApplicationService().update_status(application_id, payload.get('status', 'APPLIED'))
    return jsonify({'success': True, 'message': 'Status updated', 'data': application})


@application_api_bp.route('/jobs/<job_id>/apply', methods=['POST'])
def apply(job_id):
    payload = request.get_json(silent=True) or {}
    application = ApplicationService().apply(payload.get('candidate_id', ''), job_id)
    return jsonify({'success': True, 'message': 'Application submitted successfully', 'data': application}), 201
