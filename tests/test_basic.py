from app import create_app
from app.config import TestingConfig


def test_health():
    app = create_app(TestingConfig)
    client = app.test_client()
    response = client.get('/health')
    assert response.status_code == 200
    assert response.get_json()['status'] == 'ok'


def test_non_test_app_requires_mongodb():
    class MissingMongoConfig:
        TESTING = False
        SECRET_KEY = 'test-secret'
        MONGO_URI = ''
        MONGO_DATABASE = 'Hirehub'

    try:
        create_app(MissingMongoConfig)
    except RuntimeError as exc:
        assert 'MONGO_URI is required' in str(exc)
    else:
        raise AssertionError('Normal app startup must not silently use in-memory storage')


def test_register_and_login():
    app = create_app(TestingConfig)
    client = app.test_client()
    payload = {'name': 'Test User', 'email': 'testuser@example.com', 'phone': '9876543210', 'password': 'secret123', 'role': 'CANDIDATE'}
    register = client.post('/api/auth/register', json=payload)
    assert register.status_code == 201
    login = client.post('/api/auth/login', json={'email': 'testuser@example.com', 'password': 'secret123'})
    assert login.status_code == 200
    assert login.get_json()['success'] is True


def test_default_demo_accounts_and_admin_registration_protection():
    app = create_app(TestingConfig)
    client = app.test_client()

    accounts = [
        ('admin@hirehub.com', 'Admin@123', 'ADMIN'),
        ('recruiter@hirehub.com', 'Recruiter@123', 'RECRUITER'),
        ('candidate@hirehub.com', 'Candidate@123', 'CANDIDATE'),
    ]
    for email, password, role in accounts:
        login = client.post('/api/auth/login', json={
            'email': email,
            'password': password,
        })
        assert login.status_code == 200
        assert login.get_json()['data']['role'] == role

    register = client.post('/api/auth/register', json={
        'name': 'Public Admin',
        'email': 'public-admin@example.com',
        'phone': '9876543210',
        'password': 'StrongPass123',
        'role': 'ADMIN',
    })
    assert register.status_code == 400


def test_role_menus_and_pages_are_available_to_their_roles():
    app = create_app(TestingConfig)
    pages = {
        'candidate@hirehub.com': (
            'Candidate@123',
            ['/dashboard/', '/candidate/profile', '/candidate/resume',
             '/candidate/applications', '/candidate/saved',
             '/candidate/interviews', '/candidate/notifications'],
            ['Find jobs', 'My profile', 'Resume', 'Applications', 'Saved jobs'],
        ),
        'recruiter@hirehub.com': (
            'Recruiter@123',
            ['/recruiter/dashboard', '/recruiter/jobs', '/recruiter/jobs/new',
             '/recruiter/applicants', '/recruiter/company',
             '/recruiter/interviews', '/recruiter/analytics'],
            ['My jobs', 'Post a job', 'Applicants', 'Company', 'Analytics'],
        ),
        'admin@hirehub.com': (
            'Admin@123',
            ['/admin/dashboard', '/admin/users', '/admin/companies',
             '/admin/jobs', '/admin/applications', '/admin/reports',
             '/admin/analytics', '/admin/audit-logs'],
            ['Users', 'Companies', 'Applications', 'Reports', 'Audit logs'],
        ),
    }

    for email, (password, paths, menu_items) in pages.items():
        client = app.test_client()
        login = client.post('/api/auth/login', json={'email': email, 'password': password})
        assert login.status_code == 200
        for path in paths:
            assert client.get(path).status_code == 200, path
        homepage = client.get('/dashboard/', follow_redirects=True).get_data(as_text=True)
        for item in menu_items:
            assert item in homepage


def test_recruiter_job_candidate_application_and_interview_flow():
    app = create_app(TestingConfig)
    recruiter_client = app.test_client()
    recruiter_login = recruiter_client.post('/api/auth/login', json={
        'email': 'recruiter@hirehub.com',
        'password': 'Recruiter@123',
    })
    recruiter_id = recruiter_login.get_json()['data']['id']
    response = recruiter_client.post('/recruiter/jobs/new', data={
        'title': 'Backend Engineer',
        'description': 'Build web services.',
        'location': 'Remote',
        'skills': 'Python, Flask',
        'experience_min': '1',
        'experience_max': '5',
        'salary_min': '50000',
        'salary_max': '100000',
        'work_mode': 'REMOTE',
        'employment_type': 'FULL_TIME',
    })
    assert response.status_code == 302

    job = next(
        job for job in app.config['DATA_STORE']['jobs'].values()
        if job.get('recruiter_id') == recruiter_id and job.get('title') == 'Backend Engineer'
    )
    candidate_client = app.test_client()
    candidate_login = candidate_client.post('/api/auth/login', json={
        'email': 'candidate@hirehub.com',
        'password': 'Candidate@123',
    })
    candidate_id = candidate_login.get_json()['data']['id']
    assert candidate_client.post(f"/jobs/{job['id']}/apply").status_code == 302
    application = next(
        item for item in app.config['DATA_STORE']['applications'].values()
        if item.get('candidate_id') == candidate_id and item.get('job_id') == job['id']
    )
    application_count = len(app.config['DATA_STORE']['applications'])
    duplicate_response = candidate_client.post(f"/jobs/{job['id']}/apply", follow_redirects=True)
    assert duplicate_response.status_code == 200
    assert 'You already applied' in duplicate_response.get_data(as_text=True)
    assert 'Apply now' not in duplicate_response.get_data(as_text=True)
    assert len(app.config['DATA_STORE']['applications']) == application_count

    response = recruiter_client.post('/recruiter/interviews', data={
        'application_id': application['id'],
        'date': '2026-11-01',
        'time': '10:30',
        'type': 'ONLINE',
        'meeting_link': 'https://example.test/meeting',
    })
    assert response.status_code == 302
    assert app.config['DATA_STORE']['applications'][application['id']]['status'] == 'INTERVIEW_SCHEDULED'
    assert any(
        notification.get('user_id') == candidate_id
        and notification.get('title') == 'Interview scheduled'
        for notification in app.config['DATA_STORE']['notifications'].values()
    )
