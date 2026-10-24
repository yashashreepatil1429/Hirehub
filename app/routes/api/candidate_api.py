from flask import Blueprint, jsonify, request

from app.services.candidate_service import CandidateService


candidate_api_bp = Blueprint('candidate_api', __name__, url_prefix='/api/candidates')


@candidate_api_bp.route('/<candidate_id>', methods=['GET'])
def get_candidate(candidate_id):
    profile = CandidateService().profile(candidate_id)
    return jsonify({'success': True, 'data': profile or {}})


@candidate_api_bp.route('/<candidate_id>', methods=['PUT'])
def update_candidate(candidate_id):
    data = request.get_json(silent=True) or {}
    candidate = CandidateService().save_profile(candidate_id, data)
    return jsonify({'success': True, 'message': 'Profile updated', 'data': candidate})
