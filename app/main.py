from fastapi import FastAPI
from functions import (is_valid_id_number, 
                       get_age_from,
                       get_gender_from,
                       run_awk
                       )
from typing import Dict

description = """
    This is a simple API that allows you to validate 
    Norwegian ID numbers, retrieve the age, gender and
    check if the id number is in the database.

    ## Endpoints:
    
    - /validate/{id_number}
        You will be able to check if the id number is valid.
    - /gender/{id_number}
        You will be able to obtain the gender of the person.
    - /age/{id_number}
        You will be able to obtain the age of the person.
    - /search/{id_number}
        You will be able to search for the id number in the database.
    - /retrieve_valid_id_numbers
        You will be able to retrieve the total number of valid 
        id numbers in the database.
    - /retrieve_stratified_valid_numbers
        You will be able to retrieve the number of valid 
        id numbers stratified by gender and age groups.

"""

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

@app.get("/")
async def root():
    return {"message": "Sigma API is up and running!"}


# check if an id number is valid
@app.post("/validate/{id_number}")
async def validate(id_number: str) -> Dict:
    """
    This endpoint returns if id_number is a valid Norwegian ID number
    """

    # check if the id number is valid
    response = { "valid": is_valid_id_number(id_number)}

    # use jsonfy from 
    return response

@app.post("/gender/{id_number}")
async def gender(id_number: str) -> Dict:
    """
    This endpoint returns the gender based on the id_number
    """

    response = {'gender': get_gender_from(id_number)}

    return response

@app.post("/age/{id_number}")
async def age(id_number: str) -> Dict:
    """
    This endpoint returns the age of a person given their id number
    """

    response = {'age': get_age_from(id_number)}

    # use jsonfy from 
    return response

@app.post("/search/{id_number}")
async def search(id_number: str) -> Dict[str, list]:
    """
    This endpoint tells in which row the id_number is in the database
    """
    filename = 'data/fnr.txt'

    # we are running asyncio code, so we need to await the result
    result = await run_awk(filename, id_number)

    # Parse the output to get only the list of line numbers
    line_numbers = result.strip().split('\n') if result else []

    return {"lines": line_numbers}


@app.get("/retrieve_valid_id_numbers")
async def retrieve_valid_id_numbers() -> Dict[str, int]:
    """
    This endpoint returns all the valid id numbers in the database
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

@app.get("/retrieve_stratified_valid_numbers")
async def retrieve_stratified_valid_numbers() -> Dict[str, object]:
    """
    This endpoint returns the number of valid id numbers
    stratified by gender and tripartite age groups. We
    choose to stratify the age groups in three categories:
    - 0-19, 20-64 and >= 65 years old
    This standard is used by the Statistikk Sentralbyrå.
    """
    filename = 'data/fnr.txt'

    # we will use a dictionary to store the counts
    
    valid_numbers = {
                        'male': 0,
                        'female': 0,
                        'age_groups': 
                        {
                           '0-19': 0, 
                            '20-64': 0,
                            '>=65': 0
                        }
                    }
    
    with open(filename, 'r') as file:
        for line in file:
            if is_valid_id_number(line.strip()):
                valid_numbers[get_gender_from(line.strip())] += 1
                age = get_age_from(line.strip())
                if age < 20:
                    valid_numbers['age_groups']['0-19'] += 1
                elif age < 65:
                    valid_numbers['age_groups']['20-64'] += 1
                else:
                    valid_numbers['age_groups']['>=65'] += 1
    
    print(valid_numbers)
    return valid_numbers
    

if __name__ =='__main__':
    # run rest api with uvicorn
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8070)