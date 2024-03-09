from fastapi import FastAPI
from functions import (is_valid_id_number, 
                       get_age_from
                       )
from typing import Dict
app = FastAPI()

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

@app.post("/age/{id_number}")
async def age(id_number: str) -> Dict:
    """
    This endpoint returns the age of a person given their id number
    """

    # check if the id number is valid
    response = { "message": "This endpoint is not yet implemented"}

    response = {'age': get_age_from(id_number)}

    # use jsonfy from 
    return response



if __name__ =='__main__':
    # run rest api with uvicorn
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8070)