from fastapi import FastAPI
from app.backend import (is_valid_id_number, 
                       get_age_from,
                       get_gender_from,
                       run_awk,
                       stratified_valid_numbers,
                       TimingMiddleware
                       )
from pydantic import BaseModel, Field

from typing import Dict

description = " \n ## Endpoints: \n - **/validate/{id_number}** \n  You will be able to check if the id number is valid.\n- **/gender/{id_number}**\n    You will be able to obtain the gender of the person.\n - **/age/{id_number}** You will be able to obtain the age of the person.\n - **/search/{id_number}** You will be able to search for the id number in the database.\n - **/retrieve_valid_id_numbers** You will be able to retrieve the total number of valid id numbers in the database.\n - **/retrieve_stratified_valid_numbers**\n You will be able to retrieve the number of valid \n id numbers stratified by gender and age groups."

app = FastAPI(title="Sigma API",
    description=description,
    summary="This is a simple API to work with Norwegian ID numbers.",
    version="0.0.1",
    terms_of_service="Check the MIT license.",
    contact={
        "name": "Mauricio Moreira Soares",
        "url": "http://phydev.github.io",
        "email": "phydev@protonmail.ch",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/license/mit",
    },)

app.add_middleware(TimingMiddleware)

# Pydantic model definitions for the responses
class ValidateResponse(BaseModel):
    valid: bool = True

class GenderResponse(BaseModel):
    gender: str = 'female'

class AgeResponse(BaseModel):
    age: int = 32

class SearchResponse(BaseModel):
    lines: list = ['4', '5']

class ValidIdNumbers(BaseModel):
    total_valid_id_numbers: int = 34506

class AgeGroups(BaseModel):
    range_0_19: int = Field(..., alias="0-19")
    range_20_64: int = Field(..., alias="20-64")
    range_above_65: int = Field(..., alias=">=65")

class StratifiedValidNumbers(BaseModel):
    male: AgeGroups
    female: AgeGroups


@app.get("/")
async def root():
    return {"message": "Sigma API is up and running! \n For documentation access /docs (Swagger UI) or /redoc (ReDoc)"}


# check if an id number is valid
@app.post("/validate/{id_number}", response_model = ValidateResponse )
async def validate(id_number: str) -> Dict:
    """
    This endpoint returns if id_number is a valid Norwegian ID number
    """

    # check if the id number is valid
    response = { "valid": is_valid_id_number(id_number)}

    # use jsonfy from 
    return response

@app.post("/gender/{id_number}", response_model = GenderResponse)
async def gender(id_number: str) -> Dict:
    """
    This endpoint returns the gender based on the id_number
    """

    response = {'gender': get_gender_from(id_number)}

    return response

@app.post("/age/{id_number}", response_model = AgeResponse)
async def age(id_number: str) -> Dict:
    """
    This endpoint returns the age of a person given their id number
    """

    response = {'age': get_age_from(id_number)}

    # use jsonfy from 
    return response

@app.post("/search/{id_number}", response_model = SearchResponse)
async def search(id_number: str) -> Dict[str, list]:
    """
    This endpoint tells in which row the id_number is in the database
    """
    filename = 'data/fnr.txt'

    # we are running asyncio code, so we need to await the result
    line_numbers = await run_awk(filename, id_number)

    return {"lines": line_numbers}


@app.get("/retrieve_valid_id_numbers", response_model = ValidIdNumbers)
async def retrieve_valid_id_numbers() -> Dict[str, int]:
    """
    This endpoint returns the total number of 
    valid id numbers in the database
    """
    filename = 'data/fnr.txt'

    counter = 0

    # //TODO: this could be done in a more efficient way
    # using an external library or a more efficient algorithm
    # but for the size of the file we are working with, this is fine
    with open(filename, 'r') as file:
        for line in file:
            if is_valid_id_number(line.strip()):
                counter += 1
    
    response = {'total_valid_id_numbers': counter}

    return response

@app.get("/retrieve_stratified_valid_numbers", 
         response_model = StratifiedValidNumbers)
async def retrieve_stratified_valid_numbers() -> Dict[str, object]:
    """
    This endpoint returns the number of valid id numbers
    stratified by gender and tripartite age groups. We
    choose to stratify the age groups in three categories:
    - 0-19, 20-64 and >= 65 years old \n
    This standard is used by the Statistikk Sentralbyrå.
    """
    filename = 'data/fnr.txt'

    # we will use a dictionary to store the counts
    
    valid_numbers = stratified_valid_numbers(filename)
 
    return valid_numbers
    

if __name__ =='__main__':
    # run rest api with uvicorn
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8070, log_level = "info")