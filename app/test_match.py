from app.db import SessionLocal
from app.matching import get_skills
from uuid import UUID

profile_id = UUID("profile id")
db= SessionLocal()

skills=get_skills(profile_id,db)

print(skills)
