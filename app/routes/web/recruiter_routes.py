from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from app.routes.web.decorators import login_required, role_required
from app.repositories.application_repository import ApplicationRepository
from app.repositories.company_repository import CompanyRepository
from app.repositories.interview_repository import InterviewRepository
from app.repositories.job_repository import JobRepository
from app.services.analytics_service import AnalyticsService
from app.services.recruiter_service import RecruiterService
from app.services.notification_service import NotificationService
from app.services.interview_service import InterviewService


recruiter_bp = Blueprint('recruiter', __name__, url_prefix='/recruiter')


@recruiter_bp.route('/dashboard')
@login_required
@role_required('RECRUITER')
def dashboard():
    recruiter_id = session['user_id']
    jobs = [job for job in JobRepository().list_jobs() if job.get('recruiter_id') == recruiter_id]
    job_ids = {job['id'] for job in jobs}
    applications = [app for app in ApplicationRepository().list_applications() if app.get('job_id') in job_ids]
    interviews = [item for item in InterviewRepository().list_interviews() if item.get('recruiter_id') == recruiter_id]
    metrics = {
        'jobs': len(jobs),
        'open_jobs': sum(job.get('status') == 'OPEN' for job in jobs),
        'applications': len(applications),
        'shortlisted': sum(app.get('status') == 'SHORTLISTED' for app in applications),
        'interviews': len(interviews),
    }
    return render_template('dashboard/recruiter.html', metrics=metrics, jobs=jobs[:5], applications=applications[:5])


@recruiter_bp.route('/jobs')
@login_required
@role_required('RECRUITER')
def jobs():
    jobs = [job for job in JobRepository().list_jobs() if job.get('recruiter_id') == session['user_id']]
    return render_template('recruiter/jobs.html', jobs=jobs)


@recruiter_bp.route('/jobs/new', methods=['GET', 'POST'])
@login_required
@role_required('RECRUITER')
def create_job():
    if request.method == 'POST':
        data = request.form.to_dict()
        data['skills'] = [skill.strip() for skill in data.get('skills', '').split(',') if skill.strip()]
        try:
            for field in ('experience_min', 'experience_max', 'salary_min', 'salary_max'):
                data[field] = max(0, int(data.get(field) or 0))
            if not data.get('title') or not data.get('description'):
                raise ValueError('Title and description are required.')
            company = CompanyRepository().find_one({'recruiter_id': session['user_id']}) or {}
            data['company_id'] = company.get('id', '')
            RecruiterService().create_job(session['user_id'], data)
            flash('Job posted successfully.', 'success')
            return redirect(url_for('recruiter.jobs'))
        except ValueError as exc:
            flash(str(exc) if str(exc) else 'Enter valid numeric values.', 'danger')
    return render_template('jobs/create.html')


@recruiter_bp.route('/jobs/<job_id>/close', methods=['POST'])
@login_required
@role_required('RECRUITER')
def close_job(job_id):
    repository = JobRepository()
    job = repository.get_by_id(job_id)
    if not job or job.get('recruiter_id') != session['user_id']:
        flash('Job not found or you do not have access to it.', 'danger')
    else:
        job['status'] = 'CLOSED'
        repository.update_job(job_id, job)
        flash('Job closed.', 'success')
    return redirect(url_for('recruiter.jobs'))


@recruiter_bp.route('/applicants')
@login_required
@role_required('RECRUITER')
def applicants():
    jobs = {job['id']: job for job in JobRepository().list_jobs() if job.get('recruiter_id') == session['user_id']}
    applications = [app for app in ApplicationRepository().list_applications() if app.get('job_id') in jobs]
    return render_template('recruiter/applicants.html', applications=applications, jobs=jobs)


@recruiter_bp.route('/applications/<application_id>/<action>', methods=['POST'])
@login_required
@role_required('RECRUITER')
def application_action(application_id, action):
    application = ApplicationRepository().get_by_id(application_id)
    job = JobRepository().get_by_id(application.get('job_id', '')) if application else None
    if not application or not job or job.get('recruiter_id') != session['user_id']:
        flash('Application not found or you do not have access to it.', 'danger')
    elif action not in {'shortlist', 'reject', 'select'}:
        flash('Unsupported application action.', 'danger')
    else:
        application['status'] = {'shortlist': 'SHORTLISTED', 'reject': 'REJECTED', 'select': 'SELECTED'}[action]
        ApplicationRepository().update_application(application_id, application)
        NotificationService().create(
            application['candidate_id'],
            f'Application {action}ed',
            f'Your application for {job.get("title", "a job")} was {action}ed.',
        )
        flash(f'Application {action}ed.', 'success')
    return redirect(url_for('recruiter.applicants'))


@recruiter_bp.route('/company', methods=['GET', 'POST'])
@login_required
@role_required('RECRUITER')
def company():
    repository = CompanyRepository()
    company = repository.find_one({'recruiter_id': session['user_id']})
    if request.method == 'POST':
        data = request.form.to_dict()
        data['recruiter_id'] = session['user_id']
        if company:
            data.update({'recruiter_id': session['user_id'], 'id': company['id']})
            repository.update(company['id'], data)
        else:
            data['recruiter_id'] = session['user_id']
            RecruiterService().create_company(data)
            created = repository.find_one({'recruiter_id': session['user_id']})
            if created:
                company = created
        flash('Company profile saved.', 'success')
        return redirect(url_for('recruiter.company'))
    return render_template('recruiter/company.html', company=company or {})


@recruiter_bp.route('/interviews', methods=['GET', 'POST'])
@login_required
@role_required('RECRUITER')
def interviews():
    if request.method == 'POST':
        application_id = request.form.get('application_id', '')
        application = ApplicationRepository().get_by_id(application_id)
        job = JobRepository().get_by_id(application.get('job_id', '')) if application else None
        if not application or not job or job.get('recruiter_id') != session['user_id']:
            flash('Application not found or you do not have access to it.', 'danger')
            return redirect(url_for('recruiter.interviews'))
        data = request.form.to_dict()
        if not data.get('date') or not data.get('time'):
            flash('Interview date and time are required.', 'danger')
            return redirect(url_for('recruiter.interviews'))
        interview = InterviewService().schedule({
            **data,
            'application_id': application_id,
            'candidate_id': application['candidate_id'],
            'recruiter_id': session['user_id'],
        })
        application['status'] = 'INTERVIEW_SCHEDULED'
        application['interview_id'] = interview['id']
        ApplicationRepository().update_application(application_id, application)
        NotificationService().create(
            application['candidate_id'],
            'Interview scheduled',
            f'An interview for {job.get("title", "your application")} is scheduled on {interview["date"]} at {interview["time"]}.',
        )
        flash('Interview scheduled and candidate notified.', 'success')
        return redirect(url_for('recruiter.interviews'))
    items = [item for item in InterviewRepository().list_interviews() if item.get('recruiter_id') == session['user_id']]
    jobs = {job['id']: job for job in JobRepository().list_jobs() if job.get('recruiter_id') == session['user_id']}
    applications = [
        app for app in ApplicationRepository().list_applications()
        if app.get('job_id') in jobs and app.get('status') not in {'REJECTED', 'WITHDRAWN', 'SELECTED'}
    ]
    return render_template('recruiter/interviews.html', interviews=items, applications=applications, jobs=jobs)


@recruiter_bp.route('/analytics')
@login_required
@role_required('RECRUITER')
def analytics():
    recruiter_id = session['user_id']
    jobs = [job for job in JobRepository().list_jobs() if job.get('recruiter_id') == recruiter_id]
    job_ids = {job['id'] for job in jobs}
    applications = [app for app in ApplicationRepository().list_applications() if app.get('job_id') in job_ids]
    return render_template(
        'recruiter/analytics.html',
        metrics={
            'open_jobs': sum(job.get('status') == 'OPEN' for job in jobs),
            'total_jobs': len(jobs),
            'total_applications': len(applications),
            'shortlisted': sum(app.get('status') == 'SHORTLISTED' for app in applications),
        },
    )
