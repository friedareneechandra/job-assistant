from sqlalchemy import Column,String,Boolean, DateTime,Text, ForeignKey,Integer
from sqlalchemy.dialects.postgresql import UUID,ARRAY
from sqlalchemy.orm import relationship
import uuid
from app.db import engine,Base


class Job(Base):

    __tablename__= "job_lists"

    id = Column(UUID(as_uuid=True),primary_key=True, default=uuid.uuid4)
    remote_job_id= Column(String, unique= True, nullable= False)
    company = Column(String(100),nullable=False)
    position = Column(String,nullable=False)
    location = Column(String)
    tags = Column(ARRAY(String))
    apply_url = Column(Text,nullable=False)
    date = Column(DateTime,nullable=False)
    source = Column(String, nullable=False)
    description = Column(Text, nullable=False)

    print("Table is created ")
Base.metadata.create_all(engine)


class UserProfile(Base):
    __tablename__ = "profiles"
    profile_id = Column(UUID(as_uuid=True),primary_key=True, default=uuid.uuid4)

    @property
    def id(self):
        return self.profile_id

    email = Column(String(100),unique=True,nullable=False)
    password_hash =  Column(String(200),nullable=True)
    preferred_location = Column(String(100),nullable=False)
    minimum_experience = Column(Integer,nullable=False)
    job_type = Column(String(100),nullable=False)
    notification_enabled = Column(Boolean,nullable=False,)
    skills = relationship("Skill",back_populates="user")
    match_preference = Column(String(20), nullable=False, default="MEDIUM")
    employment_type = Column(String(50),nullable=False,default = "full time")
Base.metadata.create_all(engine)

class Skill(Base):
    __tablename__ = "skills"
    id = Column(UUID(as_uuid=True),primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("profiles.profile_id"), nullable=False)
    skill = Column(String(100),nullable=False)
    user = relationship("UserProfile",back_populates="skills")

Base.metadata.create_all(engine)

class Notification (Base):
    __tablename__="notifications"
    id = Column(UUID(as_uuid=True),primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("profiles.profile_id"), nullable=False)
    job_id = Column(UUID(as_uuid=True),ForeignKey("job_lists.id"),nullable=False)
    sent_at = Column(DateTime,nullable=False)
    status = Column(String(20), nullable=False)

Base.metadata.create_all(engine)