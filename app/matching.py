from sqlalchemy.orm import Session
from app.db import get_db
from app.models import *
from app.schema import *
from fastapi import APIRouter, Depends, HTTPException,Query

router = APIRouter()


def get_skills(profile_id,db:Session):
    return db.query(Skill).filter(Skill.user_id == profile_id).all()


def get_jobs(db:Session):
    return db.query(Job).all()


def get_profiles(profile_id,db):
    return db.query(UserProfile).filter(UserProfile.profile_id == profile_id).first()


def matched_jobs(profile_id,db:Session):
    recommendations=[]

    user_skill = get_skills(profile_id,db)
    profile = get_profiles(profile_id,db)

    if profile is None: raise HTTPException(status_code=404,detail= " Profile not found")
    if not user_skill: return []

    jobs = get_jobs(db)

    user_skill_set = set()

    for skills in user_skill:
        user_skill_set.add(skills.skill.strip().casefold())

    total_skill = len(user_skill_set)

    if total_skill == 0:
        return []

    for every_job in jobs:
        tags = every_job.tags or []
        position = every_job.position or ""
        description = every_job.description or ""
        job_text = (" ".join(tags) + " " + position + " " +description).casefold()

        matched_skills = set()

        for skill in user_skill_set:
            if skill in job_text:
                matched_skills.add(skill)

        matched_count = len(matched_skills)

        matched_percent = (matched_count / total_skill) * 100

        if matched_skills:
            recommendations.append({
                "company": every_job.company,
                "position": every_job.position,
                "matched_skills": sorted(matched_skills),
                "matched_count": matched_count,
                "matched_percent": round(matched_percent,2),
                "location": every_job.location

            })
    recommendations.sort(key=lambda recommendation: (recommendation["matched_percent"],recommendation["matched_count"],), reverse=True)

    return recommendations

def match_skills(user_skills,job):
    tags = job.tags or []
    position = job.position or ""
    description = job.description or ""
    job_text = (" ".join(tags) + " " + position + " " + description).casefold()

    user_skill_set = set()
    for every_skill in user_skills:
        user_skill_set.add(every_skill.skill.strip().casefold())

    matched_skills = set()
    for skill in user_skill_set:
        if skill in job_text:
            matched_skills.add(skill)

    return matched_skills

def find_matching_users(job,db:Session):
    notify_recommendations =[]

    users = db.query(UserProfile).all()

    for each_user in users:
        user_skills= get_skills(each_user.profile_id, db)
        matched_skills = match_skills(user_skills,job)
        matched_count = len(matched_skills)
        total_skill = len(user_skills)

        if total_skill == 0:
            continue

        matched_percent = ( matched_count / total_skill ) * 100

        if matched_skills:
            notify_recommendations.append({
                "profile_id": each_user.profile_id,
                "matched_skills": sorted(matched_skills),
                "matched_percent": round(matched_percent,2)
            })

    return notify_recommendations



@router.get("/recommendations/{profile_id}", response_model=list[RecommendationResponse])
def get_recommendation(profile_id: UUID, db: Session = Depends(get_db)):
    return matched_jobs(profile_id,db)



