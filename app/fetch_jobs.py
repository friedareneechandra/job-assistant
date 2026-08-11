from sqlalchemy.orm import Session
import requests
import datetime
from app.db import SessionLocal
from app.models import Job


session = SessionLocal()


url = "https://remoteok.com/api"

def fetch_jobs(db:Session):
    new_jobs=[]

    try:
        response = requests.get(url,timeout=30)
        raw_data = response.json() # now it is a list
        if (response.status_code == 200):
            print("Success")
        else:
            print(response.status_code == 404,"error")
    except Exception as e:
        print("error: ", e)

    for job in raw_data [1:]:
        try:
            remote_job_id = str(job["id"])
            job_exist = db.query(Job).filter(Job.remote_job_id == remote_job_id).first()
            print(job_exist)

            if job_exist:
                job_exist.company = job.get("company")
                job_exist.position = job["position"]
                job_exist.location = job["location"]
                job_exist.tags = job["tags"]
                job_exist.apply_url = job["apply_url"]
                job_exist.description = job["description"]
                job_exist.date = datetime.datetime.fromisoformat(job["date"])
                job_exist.source = "RemoteOk"

                print("update",job["id"])

            else:
                new_job = Job(
                    remote_job_id=remote_job_id,
                    company=job.get("company"),
                    position=job["position"],
                    apply_url=job["apply_url"],
                    location=job["location"],
                    tags=job["tags"],
                    date=datetime.datetime.fromisoformat(job["date"]),
                    source="RemoteOK",
                    description=job["description"],)

            db.add(new_job)
            new_jobs.append(new_job)
            print("Inserted: ", remote_job_id)

        except Exception as e:
            print("Error processing job: ",e)

    try:
        db.commit()
        return new_jobs
        print("Job fetched successfully.")
    except Exception as e:
        db.rollback()
        print(e)