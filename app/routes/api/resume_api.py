from flask import Blueprint, jsonify, request

from app.services.resume_service import ResumeService

resume_api_bp = Blueprint('resume_api', __name__, url_prefix='/api/resumes')


@resume_api_bp.route('', methods=['POST'])
def upload_resume():
    file = request.files.get('resume')
    candidate_id = request.form.get('candidate_id')
    record = ResumeService().save_resume(file, candidate_id)
    return jsonify({'success': True, 'message': 'Resume uploaded', 'data': record}), 201


@resume_api_bp.route('/<resume_id>', methods=['GET'])
def get_resume(resume_id):
    return jsonify({'success': True, 'data': {'resume_id': resume_id}})


@resume_api_bp.route('/<resume_id>', methods=['DELETE'])
def delete_resume(resume_id):
    return jsonify({'success': True, 'message': 'Resume deleted'})
