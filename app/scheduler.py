from apscheduler.schedulers.background import BackgroundScheduler
from app.fetch_jobs import fetch_jobs
from app.db import SessionLocal
from app.matching import find_matching_users
from app.notification import notify_user

scheduler = BackgroundScheduler()


def scheduled_fetch():
    print("schedular is working")
    db = SessionLocal()

    try:
        new_jobs = fetch_jobs(db)
        for each_job in new_jobs:
            matching_users = find_matching_users(each_job,db)
            send_note= notify_user(each_job,matching_users,db)
            print("Matching users:", matching_users)
            print("Send email: ", send_note)
        print("New Jobs Found: ", len(new_jobs))
    except Exception as e:
        print("Scheduled fetch failed: ", e)
    finally:
        db.close()

scheduler.add_job(scheduled_fetch,"interval",seconds=10)

def starts_scheduler():
    scheduler.start()

def stop_scheduler():
    scheduler.shutdown()