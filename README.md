# Σ-Project
![Build Status](https://github.com/phydev/sigma/actions/workflows/python-app.yml/badge.svg)

Sigma is an API for validating and retrieving information from Norwegian ID numbers.


## Getting started 


### Running the API with docker

Run the API server first you need to build the docker image:

```
docker build -t sigma:v1 .
```

Then you can run the FastAPI server:

```
docker run -d -p 8070:8070 sigma:v1
```

Then you can access the Swagger UI from the browser:

```
https://127.0.0.1:8070/docs
```


## Running tests

For testing we implemented unit tests in `/tests` which can be ran with `pytest`. The naming convention for the test files are `test_<name of the file to be tested>.py`, as well as the test functions `test_<name of the function to be tested>`. To run the whole test suit:

```
pytests tests/
```

## Repository structure

The repository is structured as follows:

```
.
├── app
│   ├── __init__.py
│   ├── main.py
│   ├── functions.py
├── tests
│   ├── __init__.py
│   ├── test_main.py
│   ├── test_functions.py
├── docs
├── data
│   ├── fnr.txt
├── Dockerfile
├── docker-compose.yml
├── README.md
```

## Test coverage report

<!-- Pytest Coverage Comment:Begin -->
<!-- Pytest Coverage Comment:End -->
