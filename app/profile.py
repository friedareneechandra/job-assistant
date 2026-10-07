from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.db import get_db
from app.auth import hash_password,verify_password,get_jwt_strategy, oauth2_scheme,get_current_user
from app.models import UserProfile, Skill,Notification
from app.schema import (
    UserProfileCreate,
    UserProfileResponse,
    SkillCreate,
    SkillResponse,
    NotificationResponse,
    LoginRequest, TokenResponse
)

router = APIRouter()


@router.post( "/profile",response_model=UserProfileResponse,status_code=status.HTTP_201_CREATED,)
def user_profile(profile: UserProfileCreate, db: Session = Depends(get_db)):
    existing_user= db.query(UserProfile).filter(UserProfile.email == profile.email).first()

    if existing_user:
        raise HTTPException(status_code=409,detail= "Email already exists")


    user = UserProfile(
        email=profile.email,
        password_hash=hash_password(profile.password),
        preferred_location=profile.preferred_location,
        minimum_experience=profile.minimum_experience,
        job_type=profile.job_type,
        employment_type=profile.employment_type,
        notification_enabled=profile.notification_enabled,
        match_preference=profile.match_preference,
    )
    try:
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500,detail="unable to create profile")




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

@router.get("/notifications/{user_id}", response_model=list[NotificationResponse])
def get_notification(user_id:UUID,db:Session= Depends(get_db)):

     notifications = db.query(Notification).filter(Notification.user_id == user_id).all()
     return notifications

@router.post("/auth/jwt/login", response_model= TokenResponse)
async def login(form_data:OAuth2PasswordRequestForm =Depends() ,db: Session = Depends(get_db)):
    user = (db.query(UserProfile).filter(UserProfile.email == form_data.username).first())

    if user is None:
        raise HTTPException(status_code=401,detail="Invalid email or password")

    if not user.password_hash:
        raise HTTPException(status_code=401,detail="User password is not set")

    if not verify_password(form_data.password,user.password_hash):
        raise HTTPException(status_code=401,detail="Invalid email or password")

    strategy = get_jwt_strategy()
    access_token = await strategy.write_token(user)

    return {"access_token": access_token,"token_type": "bearer"}



@router.get("/me", response_model=UserProfileResponse)
def get_me(
    current_user: UserProfile = Depends(get_current_user)
):
    return current_user