from apscheduler.schedulers.background import BackgroundScheduler
from app.fetch_jobs import fetch_jobs
from app.db import SessionLocal


scheduler = BackgroundScheduler()


def scheduled_fetch():
    print("schedular is working")
    db = SessionLocal()



    try:
        new_jobs = fetch_jobs(db)
        print("New Jobs Found: ", len(new_jobs))

        fetch_jobs(db)
    except Exception as e:
        print("Scheduled fetch failed: ", e)
    finally:
        db.close()


scheduler.add_job(scheduled_fetch,"interval",seconds=10)

def starts_scheduler():
    scheduler.start()

def stop_scheduler():
    scheduler.shutdown()