from app.models import UserProfile


def notify_user(each_job,matching_users,db):

    for user in matching_users:
        user_profile = db.query(UserProfile).filter(UserProfile.profile_id == user["profile_id"]).first()

        if not user_profile.notification_enabled:
            continue
        email = user_profile.email

        message = f""" Company: {each_job.company},
        Position: {each_job.position},
        Location: {each_job.location},
        Skills: {user['matched_skills']},
        Apply_Link: {each_job.apply_url}"""
        print("Email:",email+ ''+ "Message: ", message)

