import datetime
from uuid import UUID
from typing import Optional
from pydantic import BaseModel


class JobResponse(BaseModel):
    id: UUID
    company:str
    position:str
    location:str
    apply_url: str
    tags: list[str]
    description: Optional[ str] = None
    date: datetime.datetime

    class Config:
        from_attributes = True

print(JobResponse.model_fields)



class UserProfileCreate(BaseModel):
    email: str
    password: str
    preferred_location: str
    minimum_experience: int
    job_type: str
    employment_type : str
    notification_enabled: bool
    match_preference: str = "MEDIUM"


    class Config:
        from_attributes = True


class SkillCreate(BaseModel):
    skill: str

    class Config:
        from_attributes = True


class SkillResponse(BaseModel):
    skill: str

    class Config:
        from_attributes = True


class UserProfileResponse(BaseModel):
    profile_id: UUID
    email: str
    preferred_location: str
    minimum_experience: int
    job_type: str
    notification_enabled: bool
    skills: list[SkillResponse]
    employment_type: str

    class Config:
        from_attributes = True


class RecommendationResponse(BaseModel):
    company: str
    position: str
    location: str | None
    matched_skills: list[str]
    matched_count: int
    matched_percent: float
    experience_required: int | None
    experience_fit: str
    match_level: str


    class Config:
        from_attributes = True


class NotificationResponse(BaseModel):
    user_id : UUID
    job_id: UUID
    sent_at : datetime.datetime
    status : str

    class Config:
        from_attributes = True

class LoginRequest(BaseModel):
    email:str
    password:str

    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    access_token:str
    token_type:str


