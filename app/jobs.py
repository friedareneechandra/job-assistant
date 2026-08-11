from sqlalchemy import or_
from app.db import get_db
from app.models import *
from app.schema import *
from app.matching import matched_jobs
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException,Query


router = APIRouter()




@router.get("/jobs", response_model=list[JobResponse])
def get_jobs(page: int = Query(1, ge=1),limit: int = Query(10, ge=1, le=100),db: Session = Depends(get_db)):
    jobs = db.query(Job).offset((page-1)*limit).limit(limit).all()
    return jobs



@router.get("/jobs/{job_id}", response_model=JobResponse)
def get_job_id(job_id:UUID,db: Session = Depends(get_db)):
    select_id = db.query(Job).filter(Job.id == job_id).first()

    if select_id:
        return select_id
    else:
        raise HTTPException(status_code=404, detail="Page not found")


@router.get("/search", response_model=list[JobResponse])
def search_jobs(keyword: Optional[str] = None, company: Optional[str] = None,location: Optional[str] = None, db: Session = Depends(get_db)):
    query =db.query(Job)
    if keyword:
        query = query.filter(or_(Job.tags.any(keyword),
                                       Job.position.ilike(f"%{keyword}%"),
                                       Job.description.ilike(f"%{keyword}%"),
                                         Job.location.ilike(f"%{keyword}%")),
                                    )

    if company:
        query = query.filter(Job.company.ilike(f"%{company}%"))

    if location:
        query = query.filter(Job.location.ilike(f"%{location}%"))

    return query.all()

