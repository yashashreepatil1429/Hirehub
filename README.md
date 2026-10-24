# HireHub

HireHub is a modular Flask application for job hiring and recruitment workflows.

## Run on Windows

```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python run.py
```

Open `http://127.0.0.1:5000` after starting the app. MongoDB must be running locally,
or configure `MONGO_URI` in `.env`.

All application modules use the MongoDB database selected by `MONGO_DATABASE` in
`.env` (currently `Hirehub`). Normal app startup requires MongoDB to be reachable,
creates the application's collections and indexes, and does not fall back to
in-memory storage. In-memory storage is used only by pytest's `TestingConfig`.

## Default demo credentials

These demo accounts are initialized automatically when the app starts:

| Role | Email | Password |
| --- | --- | --- |
| Admin | `admin@hirehub.com` | `Admin@123` |
| Recruiter | `recruiter@hirehub.com` | `Recruiter@123` |
| Candidate | `candidate@hirehub.com` | `Candidate@123` |

These are development-only credentials. Change or remove them before deploying the
application publicly. Admin accounts cannot be created through public registration.

## Features

- Role-specific navigation and dashboards for candidates, recruiters, and admins
- Candidate profile, resume upload/download, job search, saved jobs, applications,
  interviews, notifications, and match-based recommendations
- Recruiter company profile, job posting/closing, applicant review, status updates,
  interview scheduling, and recruiter analytics
- Admin user activation, company verification, job/application monitoring,
  downloadable CSV reports, analytics charts, and audit-log view
- Session-based authentication, role checks, and REST APIs
- Responsive Bootstrap interface with MongoDB-backed repositories

## Role menus

- **Candidate:** Dashboard, Find jobs, My profile, Resume, Applications, Saved jobs,
  Interviews, Notifications
- **Recruiter:** Dashboard, My jobs, Post a job, Applicants, Company, Interviews,
  Analytics
- **Admin:** Dashboard, Users, Companies, Jobs, Applications, Reports, Analytics,
  Audit logs

Sign in with one of the demo accounts above to see that role's menu.
