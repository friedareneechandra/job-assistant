from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import UserProfile, Skill
from app.schema import (
    UserProfileCreate,
    UserProfileResponse,
    SkillCreate,
    SkillResponse,
)

router = APIRouter()


@router.post( "/profile",response_model=UserProfileResponse,status_code=status.HTTP_201_CREATED,)
def user_profile(profile: UserProfileCreate, db: Session = Depends(get_db)):
    user = UserProfile(
        email=profile.email,
        preferred_location=profile.preferred_location,
        minimum_experience=profile.minimum_experience,
        job_type=profile.job_type,
        notification_enabled=profile.notification_enabled,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


@router.post("/profile/{profile_id}/skills",response_model=SkillResponse,status_code=status.HTTP_201_CREATED,)
def user_skills(skill: SkillCreate,profile_id: UUID,db: Session = Depends(get_db),):
    profile = (db.query(UserProfile).filter(UserProfile.profile_id == profile_id).first())

    if profile is None:
        raise HTTPException(status_code=404,detail="Profile not found",)

    new_skill = Skill(user_id=profile_id,skill=skill.skill,)

    db.add(new_skill)
    db.commit()
    db.refresh(new_skill)

    return new_skill


@router.get("/profile/{profile_id}",response_model=UserProfileResponse,)
def get_user(profile_id: UUID,db: Session = Depends(get_db),):
    profile = (db.query(UserProfile).filter(UserProfile.profile_id == profile_id).first())

    if profile is None:
        raise HTTPException(
            status_code=404,
            detail="Profile not found",
        )

    return profile