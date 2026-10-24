from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from flask import abort, send_file
from pathlib import Path

from app.routes.web.decorators import login_required, role_required
from app.repositories.base_repository import BaseRepository
from app.repositories.job_repository import JobRepository
from app.repositories.user_repository import UserRepository
from app.services.application_service import ApplicationService
from app.services.candidate_service import CandidateService
from app.services.interview_service import InterviewService
from app.services.notification_service import NotificationService
from app.services.resume_service import ResumeService
from app.exceptions import ResumeUploadError


candidate_bp = Blueprint('candidate', __name__, url_prefix='/candidate')


@candidate_bp.route('/profile', methods=['GET', 'POST'])
@login_required
@role_required('CANDIDATE')
def profile():
    service = CandidateService()
    user_id = session['user_id']
    if request.method == 'POST':
        data = request.form.to_dict()
        data['email'] = (UserRepository().get_by_id(user_id) or {}).get('email', '')
        data['skills'] = [value.strip() for value in data.get('skills', '').split(',') if value.strip()]
        try:
            data['experience'] = max(0, int(data.get('experience') or 0))
            data['expected_salary'] = max(0, int(data.get('expected_salary') or 0))
        except ValueError:
            flash('Experience and expected salary must be valid numbers.', 'danger')
            return redirect(url_for('candidate.profile'))
        service.save_profile(user_id, data)
        flash('Profile saved.', 'success')
        return redirect(url_for('candidate.profile'))
    profile = service.profile(user_id) or {}
    user = UserRepository().get_by_id(user_id) or {}
    profile = {**user, **profile}
    return render_template('candidate/profile.html', profile=profile, user=user)


@candidate_bp.route('/applications')
@login_required
@role_required('CANDIDATE')
def applications():
    applications = ApplicationService().list_for_candidate(session['user_id'])
    jobs = {job['id']: job for job in JobRepository().list_jobs()}
    return render_template('candidate/applications.html', applications=applications, jobs=jobs)


@candidate_bp.route('/applications/<application_id>/withdraw', methods=['POST'])
@login_required
@role_required('CANDIDATE')
def withdraw_application(application_id):
    repository = ApplicationService().application_repository
    application = repository.get_by_id(application_id)
    if not application or application.get('candidate_id') != session['user_id']:
        flash('Application not found.', 'danger')
    elif application.get('status') in {'SELECTED', 'REJECTED', 'WITHDRAWN'}:
        flash('This application can no longer be withdrawn.', 'warning')
    else:
        application['status'] = 'WITHDRAWN'
        repository.update_application(application_id, application)
        flash('Application withdrawn.', 'success')
    return redirect(url_for('candidate.applications'))


@candidate_bp.route('/saved')
@login_required
@role_required('CANDIDATE')
def saved_jobs():
    candidate = CandidateService().profile(session['user_id']) or {}
    job_ids = set(candidate.get('saved_jobs', []))
    jobs = [job for job in JobRepository().list_jobs() if job.get('id') in job_ids]
    return render_template('jobs/list.html', jobs=jobs, title='Saved jobs')


@candidate_bp.route('/interviews')
@login_required
@role_required('CANDIDATE')
def interviews():
    items = InterviewService().list_for_candidate(session['user_id'])
    return render_template('candidate/interviews.html', interviews=items)


@candidate_bp.route('/notifications')
@login_required
@role_required('CANDIDATE')
def notifications():
    items = NotificationService().list_for_user(session['user_id'])
    return render_template('candidate/notifications.html', notifications=items)


@candidate_bp.route('/notifications/<notification_id>/read', methods=['POST'])
@login_required
@role_required('CANDIDATE')
def mark_notification_read(notification_id):
    service = NotificationService()
    item = service.mark_read(notification_id)
    if not item or item.get('user_id') != session['user_id']:
        flash('Notification not found.', 'warning')
    return redirect(url_for('candidate.notifications'))


@candidate_bp.route('/resume', methods=['GET', 'POST'])
@login_required
@role_required('CANDIDATE')
def resume():
    repository = BaseRepository()
    repository.collection_name = 'resumes'
    user_id = session['user_id']
    if request.method == 'POST':
        try:
            record = ResumeService().save_resume(request.files.get('resume'), user_id)
            repository.insert(record)
            CandidateService().save_profile(user_id, {'resume': record['id']})
            NotificationService().create(user_id, 'Resume uploaded', 'Your resume has been uploaded.')
            flash('Resume uploaded.', 'success')
        except ResumeUploadError as exc:
            flash(str(exc), 'danger')
        return redirect(url_for('candidate.resume'))
    resumes = [item for item in repository.find_all() if item.get('candidate_id') == user_id]
    return render_template('candidate/resume.html', resumes=resumes)


@candidate_bp.route('/resume/<resume_id>/download')
@login_required
@role_required('CANDIDATE')
def download_resume(resume_id):
    repository = BaseRepository()
    repository.collection_name = 'resumes'
    record = repository.find_by_id(resume_id)
    if not record or record.get('candidate_id') != session['user_id']:
        abort(404)
    path = Path(record['path']).resolve()
    if not path.is_file():
        abort(404)
    return send_file(path, as_attachment=True, download_name=record['original_name'])
