from pydantic import BaseModel,Field
from typing import Annotated,List

class JobDescriptionExtracted(BaseModel):
    title: Annotated[str,Field(...,description="Title of the Job")]
    skills: Annotated[List[str],Field(...,description="Skills required for the Job")]
    experience: Annotated[str,Field(...,description="Experience required for the Job")]
    location: Annotated[str,Field(...,description="Location of the Job")]
    salary_range: Annotated[str,Field(...,description="Salary Range for the Job")]
