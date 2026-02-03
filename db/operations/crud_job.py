from sqlalchemy.orm import Session
from db.models.job import Job
from schemas import job
from schemas.job import JobCreate

def store_job(session: Session, job_data:JobCreate ) -> str:
    job = Job(
        job_description=job_data.job_description,
        created_by=job_data.created_by
    )
    session.add(job)
    session.commit()
    return "job stored"


def get_all_jobs(session: Session, limit: int|None = None) -> list[Job]:
    query = session.query(Job)
    if limit is not None:
        query = query.limit(limit)
    # You do not need these operations because this is just a read operation
    # session.add(job)
    # session.commit()
    return query.all()
    #old working code 
    # jobs = session.query(Job).all()
    # return jobs