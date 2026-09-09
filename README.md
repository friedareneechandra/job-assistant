# Personal Job Hunting Assistant

A backend application built with **Python and FastAPI** that helps users discover relevant job opportunities based on their preferred role, location, and skills.

The application fetches job postings from the **RemoteOK API**, stores them in **PostgreSQL**, matches jobs against user profiles, and automatically sends email notifications when new matching jobs are discovered.

## Features

- Fetch job postings from the RemoteOK API
- Store job postings in PostgreSQL
- Create and manage user profiles
- Store user skills
- Match jobs based on preferred role
- Match jobs based on preferred location
- Calculate skill match percentage
- Classify recommendations as **HIGH, MEDIUM, or LOW**
- Return personalized job recommendations through a REST API
- Automatically check for newly available jobs using a scheduler
- Identify users whose profiles match newly discovered jobs
- Send email notifications for matching new jobs using **Resend**
- Store notification history in PostgreSQL
- Prevent duplicate notifications for the same user and job
- Test APIs using FastAPI Swagger UI

## How Job Matching Works

The recommendation system separates **job relevance** from **skill compatibility**.

A job first needs to match the user's preferred role and location. Once it is considered relevant, the user's skills are compared with the job's tags, title, and description.

```text
User Profile
     ↓
Role Matching
     ↓
Location Matching
     ↓
Skill Matching
     ↓
Calculate Skill Match %
     ↓
Match Level
     ↓
Sort Recommendations
```

### Match Levels

| Skill Match | Level |
|---|---|
| 70% - 100% | HIGH |
| 40% - 69% | MEDIUM |
| 0% - 39% | LOW |

A role- and location-compatible job can still be recommended even when the skill match is low.

For example:

```text
Preferred Role: Software Engineer
Job Role: Staff Software Engineer
Skill Match: 0%
Result: LOW match, but the job is still shown
```

## Email Notification Workflow

The application can automatically notify users when new matching jobs are discovered.

```text
Fetch Jobs
    ↓
Identify New Jobs
    ↓
Find Matching Users
    ↓
Check Notification Preference
    ↓
Send Email using Resend
    ↓
Store Notification
    ↓
Prevent Duplicate Notification
```

Notifications are only sent for newly inserted jobs, and the system checks the notification history before sending another notification for the same user and job.

## Technology Stack

- **Python**
- **FastAPI**
- **SQLAlchemy**
- **PostgreSQL**
- **Pydantic**
- **REST API**
- **RemoteOK API**
- **Resend**
- **uv**

## Project Structure

```text
job-assistant/
│
├── app/
│   ├── main.py
│   ├── db.py
│   ├── models.py
│   ├── schema.py
│   ├── fetch_jobs.py
│   ├── jobs.py
│   ├── profile.py
│   ├── matching.py
│   ├── notification.py
│   └── scheduler.py
│
├── .gitignore
├── pyproject.toml
├── uv.lock
└── README.md
```

## Database

The application uses **PostgreSQL** with **SQLAlchemy ORM**.

### Main Tables

#### `profiles`

Stores user profile information and job preferences.

Examples include:

- Email
- Preferred role
- Preferred location
- Years of experience
- Employment type
- Notification preference
- Match preference

#### `skills`

Stores skills associated with each user profile.

#### `job_lists`

Stores job postings fetched from RemoteOK.

Job information includes:

- Company
- Position
- Location
- Tags
- Description
- Application URL
- Source
- Date
- Remote job ID

#### `notifications`

Stores email notification history.

Includes:

- User
- Job
- Sent time
- Notification status

## Job Fetching

The application fetches job postings from:

`https://remoteok.com/api`

Jobs are stored in PostgreSQL using the RemoteOK job ID to prevent duplicate job records.

The fetch process distinguishes between:

- **New jobs** — inserted into the database
- **Existing jobs** — updated when applicable

Only newly inserted jobs are passed to the notification workflow.

## API

The application exposes REST API endpoints using FastAPI.

### Job Recommendations

```http
GET /recommendations/{profile_id}
```

The recommendation endpoint returns information such as:

- Company
- Position
- Location
- Matched skills
- Matched skill count
- Skill match percentage
- Match level

Example:

```json
{
  "company": "Example Company",
  "position": "Software Engineer",
  "location": "Remote",
  "matched_skills": ["python"],
  "matched_count": 1,
  "matched_percent": 50.0,
  "match_level": "MEDIUM"
}
```

The API can be tested through FastAPI's automatically generated Swagger UI.

## Scheduled Job Processing

The application includes a scheduler that periodically:

1. Fetches the latest jobs.
2. Detects newly inserted jobs.
3. Finds users whose profiles match the new jobs.
4. Sends email notifications when enabled.
5. Records notification history.
6. Prevents duplicate notifications.

## Testing

The project has been tested during development using:

- FastAPI Swagger UI
- PostgreSQL queries
- Python test scripts
- Notification duplicate checks
- Job matching tests
- Scheduler testing

## Current Development

The following features are currently being improved:

- Experience-based job matching
- Experience compatibility indicators
- Improved recommendation ranking
- More accurate skill matching
- Better job-role normalization

## Future Improvements

- JWT authentication and authorization
- Protected user-specific recommendation endpoints
- Improved skill matching and normalization
- Better experience extraction from job descriptions
- Additional job sources beyond RemoteOK
- Frontend dashboard
- Advanced recommendation ranking
- User-specific job alert settings
- Improved automated testing
- Production deployment

## What I Learned

Through this project, I have been strengthening my understanding of:

- FastAPI application architecture
- REST API development
- SQLAlchemy ORM
- PostgreSQL database design
- Pydantic validation
- Database relationships
- Recommendation and matching logic
- Scheduled background processing
- Email notification workflows
- Duplicate prevention
- API testing with Swagger
- Backend project structure

## Author

**Frieda Renee Chandra**

MCA Graduate | Python & Backend Development
