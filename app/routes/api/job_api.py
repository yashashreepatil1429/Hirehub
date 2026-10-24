from flask import Blueprint, jsonify, request

from app.services.job_service import JobService

job_api_bp = Blueprint('job_api', __name__, url_prefix='/api/jobs')


@job_api_bp.route('', methods=['GET'])
def list_jobs():
    args = request.args
    filters = {
        'location': args.get('location'),
        'work_mode': args.get('work_mode'),
        'employment_type': args.get('employment_type'),
    }
    jobs = JobService().list_jobs(filters)
    return jsonify({'success': True, 'data': jobs})


@job_api_bp.route('/<job_id>', methods=['GET'])
def get_job(job_id):
    job = JobService().get_by_id(job_id)
    return jsonify({'success': True, 'data': job or {}})


@job_api_bp.route('', methods=['POST'])
def create_job():
    payload = request.get_json(silent=True) or {}
    job = JobService().create_job(payload)
    return jsonify({'success': True, 'message': 'Job created', 'data': job}), 201


@job_api_bp.route('/<job_id>', methods=['PUT'])
def update_job(job_id):
    payload = request.get_json(silent=True) or {}
    job = JobService().update_job(job_id, payload)
    return jsonify({'success': True, 'message': 'Job updated', 'data': job})
