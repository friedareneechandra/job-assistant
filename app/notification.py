from sqlalchemy import UUID,and_
from app.models import UserProfile,Notification
from dotenv import load_dotenv
from app.db import get_db
from sqlalchemy.orm import session
from fastapi import APIRouter, Depends, HTTPException,Query
import resend, datetime
import os

router = APIRouter()

load_dotenv()


api_key = os.getenv("RESEND_API_KEY")
resend.api_key = api_key


def notify_user(each_job,matching_users,db):
        for user in matching_users:
            user_profile = db.query(UserProfile).filter(UserProfile.profile_id == user["profile_id"]).first()
            if not user_profile.notification_enabled:
                continue
            already_notified = db.query(Notification).filter(and_(Notification.user_id == user["profile_id"], Notification.job_id == each_job.id)).first()
            if already_notified:
                continue

            message = f""" Company: {each_job.company},
            Position: {each_job.position},
            Location: {each_job.location},
            Skills: {user['matched_skills']},
            Match_percent: {user["matched_percent"]},
            Apply_Link: {each_job.apply_url},
            """

            try:
                print("EMAIL VALUE:", repr(user_profile.email))
                print("EMAIL TYPE:", type(user_profile.email))
                print("EMAIL AFTER STRIP:", repr(user_profile.email.strip()))
                response = resend.Emails.send({"from": "onboarding@resend.dev",
                                "to": "mabelkart108@gmail.com",
                                "text": message,
                                "subject": "New Job Macthes Your Skill"})
                print("Notification sent to: ",user_profile.email)

                notification = Notification(user_id = user["profile_id"],
                                            job_id = each_job.id,
                                            sent_at = datetime.datetime.now() ,
                                            status = "sent")
                db.add(notification)
                db.commit()

            except Exception as e:
                db.rollback()
                print(f"Couldn't send email to:{user_profile.email} Error:{e}")



