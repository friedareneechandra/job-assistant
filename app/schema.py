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
    preferred_location: str
    minimum_experience: int
    job_type: str
    notification_enabled: bool

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

    class Config:
        from_attributes = True


class RecommendationResponse(BaseModel):
    company: str
    position: str
    location: str | None
    matched_skills: list[str]
    matched_count: int
    match_percent: float

    class Config:
        from_attributes = True


class NotificationResponse(BaseModel):
    user_id : UUID
    job_id: UUID
    sent_at : datetime.datetime
    status : str

    class Config:
        from_attributes = True
