from fastapi import FastAPI
from app.functions import is_valid_id_number
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Sigma API is up and running!"}


# check if an id number is valid
@app.post("/id_number/validate")
async def validate_id_number(id_number: int):
    """
    This endpoint returns if id_number is a  valid Norwegian ID number
    """

    # check if the id number is valid
    response = { "message": is_valid_id_number(id_number)}

    # use jsonfy from 
    return response

