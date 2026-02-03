from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
import os
from schemas.job_extract import JobDescriptionExtracted

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.environ['OPENAI_API_KEY']

def extract_job_description(job_description:str)->JobDescriptionExtracted:
    model=ChatOpenAI(name="gpt-4o-mini")
    parser=PydanticOutputParser(pydantic_object=JobDescriptionExtracted)
    template=PromptTemplate(
        input_variables=["job_description"],
        partial_variables={
            "output_schema": parser.get_format_instructions()\
        },
        template=(
            "You are an expert at extracting structured information from unstructured job description.\n"
            " Job Description:\n {job_description}:\n"
            "Extract the following fields (Output Schema):\n {output_schema}\n"
        )
    )
    prompt=template.invoke({"job_description":job_description})
    print("Prompt: \n", prompt.to_string(),"\n")
    response=model.invoke(prompt)
    final_result=parser.parse(response.content)
    print("Extracted Job Description: \n", final_result.dict(),"\n")
    return final_result
