from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from app.repositories.candidate_repository import CandidateRepository
from app.repositories.application_repository import ApplicationRepository
from app.services.application_service import ApplicationService
from app.services.candidate_service import CandidateService
from app.services.job_service import JobService
from app.routes.web.decorators import login_required, role_required
from app.exceptions import DuplicateApplicationError, HireHubError

job_bp = Blueprint('jobs', __name__, url_prefix='/jobs')


@job_bp.route('', methods=['GET'])
def list_jobs():
    filters = request.args
    jobs = JobService().search(
        keyword=filters.get('keyword', ''),
        skills=filters.get('skills', ''),
        location=filters.get('location', ''),
        work_mode=filters.get('work_mode', ''),
        employment_type=filters.get('employment_type', ''),
        company=filters.get('company', ''),
    )
    jobs = [job for job in jobs if job.get('status') == 'OPEN']
    return render_template('jobs/list.html', jobs=jobs, filters=filters, title='Find jobs')


@job_bp.route('/<job_id>')
def details(job_id):
    job = JobService().get_by_id(job_id)
    saved = False
    application = None
    if session.get('role') == 'CANDIDATE':
        profile = CandidateRepository().get_by_user_id(session['user_id']) or {}
        saved = job_id in profile.get('saved_jobs', [])
        application = ApplicationRepository().get_by_candidate_and_job(session['user_id'], job_id)
    return render_template('jobs/detail.html', job=job, saved=saved, application=application)


@job_bp.route('/new', methods=['GET', 'POST'])
def new():
    return redirect(url_for('recruiter.create_job'))


@job_bp.route('/<job_id>/apply', methods=['POST'])
@login_required
@role_required('CANDIDATE')
def apply(job_id):
    try:
        ApplicationService().apply(session['user_id'], job_id)
        flash('Application submitted successfully.', 'success')
    except DuplicateApplicationError:
        flash('You have already applied to this job. Your existing application is shown below.', 'info')
    except HireHubError as exc:
        flash(str(exc), 'warning')
    except ValueError as exc:
        flash(str(exc), 'danger')
    return redirect(url_for('jobs.details', job_id=job_id))


@job_bp.route('/<job_id>/save', methods=['POST'])
@login_required
@role_required('CANDIDATE')
def save(job_id):
    try:
        CandidateService().save_job(session['user_id'], job_id)
        flash('Job saved to your list.', 'success')
    except ValueError as exc:
        flash(str(exc), 'danger')
    return redirect(url_for('jobs.details', job_id=job_id))
