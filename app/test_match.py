from app.db import SessionLocal
from app.matching import get_skills, find_matching_users
from app.models import Job, Skill
from uuid import UUID

# profile_id = UUID("profile id")
db= SessionLocal()
print("Testing matching...")


jobs = db.query(Job).all()
for item in jobs:
    if "docker" in [tag.casefold() for tag in (item.tags or [])]:
        job = item
        break

match_users = find_matching_users(job, db)

print("Job:", job.position)
print("Tags:", job.tags)
print("Result:", match_users)
