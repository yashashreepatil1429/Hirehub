from flask import Blueprint, jsonify

from app.services.analytics_service import AnalyticsService

analytics_api_bp = Blueprint('analytics_api', __name__, url_prefix='/api/analytics')


@analytics_api_bp.route('/candidate')
def candidate_stats():
    return jsonify({'success': True, 'data': {'candidate': {'total_applications': 0}}})


@analytics_api_bp.route('/recruiter')
def recruiter_stats():
    return jsonify({'success': True, 'data': AnalyticsService().dashboard_metrics()})


@analytics_api_bp.route('/admin')
def admin_stats():
    return jsonify({'success': True, 'data': AnalyticsService().dashboard_metrics()})
