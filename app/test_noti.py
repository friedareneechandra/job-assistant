from app.db import SessionLocal
from app.matching import find_matching_users
from app.notification import notify_user
from app.models import Job

db = SessionLocal()

remote_job_ids = [
    "TEST-NOTIFY-HIGH-001",
    "TEST-NOTIFY-MEDIUM-001",
    "TEST-NOTIFY-LOW-001"
]

for remote_job_id in remote_job_ids:

    job = (
        db.query(Job)
        .filter(Job.remote_job_id == remote_job_id)
        .first()
    )

    if job is None:
        print("Job not found:", remote_job_id)
        continue

    print("\n==============================")
    print("Testing:", job.company)
    print("Position:", job.position)
    print("Tags:", job.tags)

    matching_users = find_matching_users(job, db)

    print("Matching users:", matching_users)

    notify_user(job, matching_users, db)

db.close()
