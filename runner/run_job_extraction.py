from services.extract import extract_job_description
from schemas.job_extract import JobDescriptionExtracted
from db.operations.crud_job import get_all_jobs
from db.session import get_db

def run_db():
    session = next(get_db())
    jobs = get_all_jobs(session, limit=1)
    for job in jobs:
        print(job.job_description)
        result = extract_job_description(job.job_description)
        print(job.id, result)

def run():
    extract_job_description("Looking for a backend developer with experience in Python and FastAPI. The job is located in New York and offers a salary range of $80,000 to $120,000 per year. Minimum experience required is 3 years.")

if __name__ == "__main__":
    run_db()