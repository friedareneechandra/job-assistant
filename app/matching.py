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


def calculate_experience_fit(user_experience,job_experience):
    if job_experience is None:
        return "UNKNOWN"
    if user_experience >= job_experience:
        return "GOOD"

    difference = job_experience -  user_experience
    if difference <= 2:
        return "SLIGHTLY ABOVE"

    return "LOW"



def estimate_job_experience(job):
    position =  (job.position or "").casefold()
    tags = job.tags or []
    text = "".join(tags).casefold() + " " + position

    if "intern" in text or "internship" in text:
        return 0
    if "entry level" in text or "junior" in text:
        return 0
    if "associate" in text:
        return 1
    if "mid" in text:
        return 2
    if "senior" in text or "iii" in text:
        return 4
    if "staff" in text or "lead" in text or "principal" in text:
        return 5
    if " ii " in f"{position}":
        return 2

    return None

def get_match_level(matched_percent):
    if matched_percent >= 70:
        return  "HIGH"
    elif matched_percent >= 40:
        return "MEDIUM"
    else:
        return "LOW"



def matched_jobs(profile_id,db:Session):
    recommendations=[]

    user_skill = get_skills(profile_id,db)
    profile = get_profiles(profile_id,db)

    print("Profile:",profile.job_type,profile.preferred_location)
    print("User Skills:",[s.skill for s in user_skill])


    if profile is None: raise HTTPException(status_code=404,detail= " Profile not found")
    if not user_skill: return []

    jobs = get_jobs(db)
    print("Total jobs:",len(jobs))


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
        location =  every_job.location or ""

        preferred_role = profile.job_type.strip().casefold()

        job_position = position.strip().casefold()
        user_preferred_location = profile.preferred_location.strip().casefold()
        job_location = location.strip().casefold()

        print("CHECKING:", position, "|", location)
        print("ROLE:", preferred_role, "vs", job_position)

        if preferred_role not in job_position:
            print("  -> REJECTED: ROLE")
            continue



        if not (user_preferred_location in job_location
                or "remote" in job_location
                or "hybrid" in job_location
                or "worldwide" in job_location):
            print("  -> REJECTED: LOCATION")
            continue

        job_experience = estimate_job_experience(every_job)
        experience_fit = calculate_experience_fit(profile.minimum_experience,job_experience)

        job_text = (" ".join(tags) + " " + position + " " +description).casefold()

        matched_skills = set()

        for skill in user_skill_set:
            if skill in job_text:
                matched_skills.add(skill)

        matched_count = len(matched_skills)

        matched_percent = (matched_count / total_skill) * 100

        match_level = get_match_level(matched_percent)

        print(
            "  -> ACCEPTED:",
            position,
            "skills =", matched_skills,
            "percent =", matched_percent,
            "level =", match_level
        )

        recommendations.append({
            "company": every_job.company,
            "position": every_job.position,
            "matched_skills": sorted(matched_skills),
            "matched_count": matched_count,
            "matched_percent": round(matched_percent, 2),
            "match_level": match_level,
            "location": every_job.location,
            "experience_required": job_experience,
            "experience_fit": experience_fit
        })



    recommendations.sort(key=lambda recommendation: (recommendation["matched_percent"],recommendation["matched_count"],), reverse=True)

    return recommendations

def match_skills(user_skills,job):
    tags = job.tags or []
    position = job.position or ""
    description = job.description or ""
    job_text = ("".join(tags) + " " + position + " " + description).casefold()

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
        if not user_skills:
            continue

        #-----------------
        # Role matching
        #-----------------

        preferred_role =  each_user.job_type.strip().casefold()
        job_position =  (job.position or "").strip().casefold()

        if preferred_role not in job_position:
            continue

        # -----------------
        # Location matching
        # -----------------

        user_preferred_location = (each_user.preferred_location.strip().casefold())
        job_location = (job.location or "").strip().casefold()

        if not (user_preferred_location in job_location
                or "remote" in job_location
                or "hybrid" in job_location
                or "worldwide" in job_location):
            continue

        #---------------
        #Skill matching
        #---------------

        matched_skills = match_skills(user_skills,job)

        user_skill_set = {
            skill.skill.strip().casefold()
            for skill in user_skills
        }
        total_skill = len(user_skill_set)

        if total_skill == 0:
            continue

        matched_count = len(matched_skills)
        matched_percent = ( matched_count / total_skill ) * 100

        match_level =  get_match_level(matched_percent)



        # preference_priority = {"HIGH": 3, "MEDIUM": 2, "LOW": 1}
        #
        # user_priority = preference_priority[each_user.match_preference]
        # job_priority = preference_priority[match_level]
        #
        # if job_priority < user_priority:
        #     continue

        notify_recommendations.append({
            "profile_id": each_user.profile_id,
            "matched_skills": sorted(matched_skills),
            "matched_percent": round(matched_percent,2),
            "match_level": match_level
        })

    return notify_recommendations


@router.get("/recommendations/{profile_id}", response_model=list[RecommendationResponse])
def get_recommendation(profile_id: UUID, db: Session = Depends(get_db)):
    return matched_jobs(profile_id,db)



if __name__ == "__main__":
    from app.db import SessionLocal

    db = SessionLocal()

    jobs = get_jobs(db)

    for job in jobs:
        experience = estimate_job_experience(job)

        if "software engineer" in (job.position or "").casefold():
            print(job.position, "→", experience)

    db.close()