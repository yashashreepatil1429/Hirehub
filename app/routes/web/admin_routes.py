from flask import Blueprint, Response, flash, redirect, render_template, session, url_for

from app.routes.web.decorators import login_required, role_required
from app.repositories.application_repository import ApplicationRepository
from app.repositories.base_repository import BaseRepository
from app.repositories.company_repository import CompanyRepository
from app.repositories.job_repository import JobRepository
from app.repositories.user_repository import UserRepository
from app.services.report_service import ReportService


admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


@admin_bp.route('/dashboard')
@login_required
@role_required('ADMIN')
def dashboard():
    users = UserRepository().list_users()
    jobs = JobRepository().list_jobs()
    applications = ApplicationRepository().list_applications()
    companies = CompanyRepository().list_companies()
    metrics = {
        'users': len(users),
        'candidates': sum(user.get('role') == 'CANDIDATE' for user in users),
        'recruiters': sum(user.get('role') == 'RECRUITER' for user in users),
        'companies': len(companies),
        'jobs': len(jobs),
        'applications': len(applications),
    }
    return render_template('dashboard/admin.html', metrics=metrics)


@admin_bp.route('/users')
@login_required
@role_required('ADMIN')
def users():
    return render_template('admin/users.html', users=UserRepository().list_users())


@admin_bp.route('/users/<user_id>/toggle', methods=['POST'])
@login_required
@role_required('ADMIN')
def toggle_user(user_id):
    if user_id == session['user_id']:
        flash('You cannot deactivate your own admin account.', 'warning')
    else:
        repository = UserRepository()
        user = repository.get_by_id(user_id)
        if not user:
            flash('User not found.', 'danger')
        else:
            repository.update_user(user_id, {'is_active': not user.get('is_active', True)})
            flash('User status updated.', 'success')
    return redirect(url_for('admin.users'))


@admin_bp.route('/companies')
@login_required
@role_required('ADMIN')
def companies():
    return render_template('admin/companies.html', companies=CompanyRepository().list_companies())


@admin_bp.route('/companies/<company_id>/verify', methods=['POST'])
@login_required
@role_required('ADMIN')
def verify_company(company_id):
    repository = CompanyRepository()
    company = repository.get_by_id(company_id)
    if company:
        repository.update(company_id, {'verified': not company.get('verified', False)})
        flash('Company verification status updated.', 'success')
    else:
        flash('Company not found.', 'danger')
    return redirect(url_for('admin.companies'))


@admin_bp.route('/jobs')
@login_required
@role_required('ADMIN')
def jobs():
    return render_template('admin/jobs.html', jobs=JobRepository().list_jobs())


@admin_bp.route('/applications')
@login_required
@role_required('ADMIN')
def applications():
    return render_template('admin/applications.html', applications=ApplicationRepository().list_applications())


@admin_bp.route('/reports')
@login_required
@role_required('ADMIN')
def reports():
    return render_template(
        'admin/reports.html',
        users=UserRepository().list_users(),
        jobs=JobRepository().list_jobs(),
        applications=ApplicationRepository().list_applications(),
    )


@admin_bp.route('/reports/<report_type>.csv')
@login_required
@role_required('ADMIN')
def report_csv(report_type):
    reports = {
        'candidates': [
            {key: user.get(key) for key in ('id', 'name', 'email', 'phone', 'role', 'is_active', 'created_at')}
            for user in UserRepository().list_users()
            if user.get('role') == 'CANDIDATE'
        ],
        'jobs': JobRepository().list_jobs(),
        'applications': ApplicationRepository().list_applications(),
    }
    rows = reports.get(report_type)
    if rows is None:
        return {'success': False, 'message': 'Report not found', 'error_code': 'REPORT_NOT_FOUND'}, 404
    csv_content = ReportService.generate_csv(rows)
    return Response(
        csv_content,
        mimetype='text/csv',
        headers={'Content-Disposition': f'attachment; filename=hirehub-{report_type}.csv'},
    )


@admin_bp.route('/analytics')
@login_required
@role_required('ADMIN')
def analytics():
    from app.services.analytics_service import AnalyticsService

    service = AnalyticsService()
    return render_template(
        'admin/analytics.html',
        metrics=service.dashboard_metrics(),
        jobs_by_location=service.jobs_by_location(),
        applications_by_status=service.applications_by_status(),
    )


@admin_bp.route('/audit-logs')
@login_required
@role_required('ADMIN')
def audit_logs():
    repository = BaseRepository()
    repository.collection_name = 'audit_logs'
    return render_template('admin/audit_logs.html', logs=repository.find_all(sort_by='timestamp'))
