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
        if user_profile is None:
            continue

        if not user_profile.notification_enabled:
            continue

        preference_priority = {"LOW": 1, "MEDIUM": 2, "HIGH": 3}
        user_priority = preference_priority[user_profile.match_preference.strip().upper()]
        job_priority = preference_priority[user["match_level"].strip().upper()]

        if job_priority < user_priority:
            print(f"Skip notification for {user_profile.email}:"
                  f"{user['match_level']} <" f"{user_profile.match_preference}")
            continue




        already_notified = db.query(Notification).filter(and_(Notification.user_id == user["profile_id"], Notification.job_id == each_job.id)).first()
        if already_notified:
            print (f"Already notified{user_profile}"
                   f"for job {each_job}")
            continue


        message = f"""
        New Job Match Found!

        Company: {each_job.company}
        Position: {each_job.position}
        Location: {each_job.location}

        Matched Skills: {", ".join(user["matched_skills"]) if user["matched_skills"] else "No direct skill match"}
        Match Percentage: {user["matched_percent"]}%
        Match Level: {user["match_level"]}

        Apply Here:
        {each_job.apply_url}

        This job was recommended based on your preferred role and location.
        """

        try:
            response = resend.Emails.send({"from": "onboarding@resend.dev",
                            "to": "mabelkart108@gmail.com",
                            "text": message,
                            "subject": "New Job Macthes Your Profile"})

            print("RESEND RESPONSE:", response)
            print("Notification sent to: ",user_profile.email)
            print("NOTIFICATION ENABLED:", user_profile.notification_enabled)
            print("JOB:", each_job.position)
            print("MATCHING DATA:", user)
            print("SENDING EMAIL...")


            notification = Notification(user_id = user["profile_id"],
                                        job_id = each_job.id,
                                        sent_at = datetime.datetime.now() ,
                                        status = "sent")
            db.add(notification)
            db.commit()

        except Exception as e:
            db.rollback()
            print(f"Couldn't send email to:{user_profile.email} Error:{e}")



