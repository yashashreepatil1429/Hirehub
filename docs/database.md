# Database

HireHub loads the repository-root `.env` file using `python-dotenv`. Set
`MONGO_URI` and `MONGO_DATABASE` there to choose the MongoDB server and database.
The local `.env` connects to `mongodb://127.0.0.1:27017` and uses the `Hirehub`
database. MongoDB database names are case-insensitive on Windows; use the same
casing as any database already created on that server. MongoDB must be running
before starting the app.

Repositories use MongoDB collections when a URI is configured. The in-memory
store is reserved for pytest's `TestingConfig`; normal app startup requires a
working MongoDB connection and fails with a clear error if MongoDB is unavailable.
Startup creates the app's collections and indexes in the database named by
`MONGO_DATABASE`.

Collections used by the application include `users`, `candidates`, `recruiters`,
`companies`, `jobs`, `applications`, `interviews`, `resumes`, `notifications`,
and `audit_logs`.

The user email and candidate/job application pair have unique indexes. Jobs have
indexes for title, skills, and location; applications are indexed by candidate
and job. Analytics summaries and label charts use MongoDB counts and aggregation
pipelines.
