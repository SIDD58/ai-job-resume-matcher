from pydantic import BaseModel,Field,field_validator
from typing import Annotated
class JobCreate(BaseModel):
    job_description:Annotated[str,Field(...,description="Description of the Job",examples=['Looking for a backend developer with experience in Python and FastAPI.'])]
    created_by:Annotated[str,Field(...,description="Created by which User",examples=["sid","ives"])]
    @field_validator('job_description','created_by')
    @classmethod
    def trim_and_lowercase(cls,value:str):
        return value.strip().lower()