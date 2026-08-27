from app.models import UserProfile
from dotenv import load_dotenv
import resend
import os


load_dotenv()

api_key = os.getenv("RESEND_API_KEY")
resend.api_key = api_key

def notify_user(each_job,matching_users,db):

        for user in matching_users:
            user_profile = db.query(UserProfile).filter(UserProfile.profile_id == user["profile_id"]).first()
            if not user_profile.notification_enabled:
                continue
            message = f""" Company: {each_job.company},
            Position: {each_job.position},
            Location: {each_job.location},
            Skills: {user['matched_skills']},
            Apply_Link: {each_job.apply_url} """

            try:
                print("EMAIL VALUE:", repr(user_profile.email))
                print("EMAIL TYPE:", type(user_profile.email))
                print("EMAIL AFTER STRIP:", repr(user_profile.email.strip()))
                response = resend.Emails.send({"from": "onboarding@resend.dev",
                                "to": user_profile.email.strip(),
                                "text": message,
                                "subject": "New Job Macthes Your Skill"})
                print("Notification sent to: ",user_profile.email)

            except Exception as e:
                print(f"Couldn't send email to:{user_profile.email} Error:{e}")
