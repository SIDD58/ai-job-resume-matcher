from pydantic import BaseModel,Field,field_validator,computed_field
from typing import List,Annotated

class ProjectCreate(BaseModel):
    title:Annotated[str,Field(...,description="Title of the Project",examples=['fitness tracker'])]
    description:Annotated[str,Field(...,description="Description of the Project",examples=['project is about ecommerce'])]
    tech_stack:Annotated[List[str],Field(...,description="List of skills",examples=[['C++','Python'],['Java']])]
    created_by:Annotated[str,Field(...,description="Created by which User",examples=["sid","ives"])]

    @field_validator('title','description','created_by')
    @classmethod
    def trim_and_lowercase(cls,value:str):
        return value.strip().lower()
    
    @field_validator('tech_stack')
    @classmethod
    def trim_and_lowercase_list(cls,values:List[str]):
        values=[value.strip().lower() for value in values]
        return values
    
    @computed_field
    @property
    def searchable_text(self)->str:
        return (
            f"title: {self.title}, "
            f"description: {self.description}, "
            f"tech_stack: {self.tech_stack} "
        )
    

class ProjectGet(BaseModel):
    title: Annotated[str, Field(..., description="Title of the Project")]
    description: Annotated[str, Field(..., description="Description of the Project")]
    tech_stack: Annotated[List[str], Field(..., description="List of skills")]

    @field_validator('title','description')
    @classmethod
    def trim_and_lowercase(cls,value:str):
        return value.strip().lower()
    
    @field_validator('tech_stack')
    @classmethod
    def trim_and_lowercase_list(cls,values:List[str]):
        values=[value.strip().lower() for value in values]
        return values


    


