from flask import Blueprint, jsonify, request

from app.services.interview_service import InterviewService

interview_api_bp = Blueprint('interview_api', __name__, url_prefix='/api/interviews')


@interview_api_bp.route('', methods=['POST'])
def create_interview():
    payload = request.get_json(silent=True) or {}
    interview = InterviewService().schedule(payload)
    return jsonify({'success': True, 'message': 'Interview scheduled', 'data': interview}), 201


@interview_api_bp.route('', methods=['GET'])
def list_interviews():
    return jsonify({'success': True, 'data': InterviewService().interview_repository.list_interviews()})


@interview_api_bp.route('/<interview_id>', methods=['PUT'])
def update_interview(interview_id):
    payload = request.get_json(silent=True) or {}
    interview = InterviewService().interview_repository.update_interview(interview_id, payload)
    return jsonify({'success': True, 'message': 'Interview updated', 'data': interview})
