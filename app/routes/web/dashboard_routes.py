from flask import Blueprint, render_template, session

from app.repositories.application_repository import ApplicationRepository
from app.repositories.candidate_repository import CandidateRepository
from app.repositories.interview_repository import InterviewRepository
from app.repositories.job_repository import JobRepository
from app.services.matching_service import MatchingService
from app.services.recommendation_service import RecommendationService
from app.routes.web.decorators import login_required


dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')


@dashboard_bp.route('/')
@login_required
def index():
    role = session.get('role', 'CANDIDATE')
    if role == 'RECRUITER':
        from flask import redirect, url_for
        return redirect(url_for('recruiter.dashboard'))
    if role == 'ADMIN':
        from flask import redirect, url_for
        return redirect(url_for('admin.dashboard'))
    user_id = session['user_id']
    profile = CandidateRepository().get_by_user_id(user_id) or {}
    applications = [item for item in ApplicationRepository().list_applications() if item.get('candidate_id') == user_id]
    interviews = [item for item in InterviewRepository().list_interviews() if item.get('candidate_id') == user_id]
    completion_fields = ('name', 'phone', 'location', 'skills', 'education', 'experience', 'expected_salary')
    completion = round(sum(bool(profile.get(key)) for key in completion_fields) * 100 / len(completion_fields))
    metrics = {
        'profile_completion': completion,
        'applications': len(applications),
        'shortlisted': sum(item.get('status') == 'SHORTLISTED' for item in applications),
        'interviews': len(interviews),
    }
    recommendations = RecommendationService().recommend_jobs(
        profile,
        [job for job in JobRepository().list_jobs() if job.get('status') == 'OPEN'],
    )[:4] if profile else []
    return render_template('dashboard/candidate.html', metrics=metrics, recommendations=recommendations)
