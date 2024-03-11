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

## Test Coverage & Performance report - 11.03.2024

```
---------- coverage: platform linux, python 3.10.13-final-0 ----------
Name               Stmts   Miss  Cover   Missing
------------------------------------------------
app/functions.py      80     11    86%   18, 20, 22, 24, 125, 191-202
app/main.py           73      6    92%   98-106, 173-175
------------------------------------------------
TOTAL                153     17    89%


============================= slowest 10 durations =============================
21.03s call     tests/test_main.py::test_retrieve_stratified_valid_numbers
14.64s call     tests/test_main.py::test_retrieve_valid_id_numbers
0.05s call     tests/test_main.py::test_root

(7 durations < 0.005s hidden.  Use -vv to show these durations.)
======================== 14 passed, 1 warning in 36.67s ========================
```