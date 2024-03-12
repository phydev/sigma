# Σ-Project
![Build Status](https://github.com/phydev/sigma/actions/workflows/python-app.yml/badge.svg)
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>

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
│   ├── backend.py
├── tests
│   ├── __init__.py
│   ├── test_main.py
│   ├── test_backend.py
├── docs
├── data
│   ├── fnr.txt
│   ├── test_data.txt
├── .github
|   ├── workflows
│       ├── python-app.yml 
├── Dockerfile
├── compose-dev.yaml
├── README.md
```

## Test Coverage & Performance report - 12.03.2024

```
---------- coverage: platform linux, python 3.10.13-final-0 ----------
Name             Stmts   Miss  Cover   Missing
----------------------------------------------
app/backend.py     112      6    95%   25, 27, 29, 31, 128, 207
app/main.py         62      5    92%   117-122, 168-170
----------------------------------------------
TOTAL              174     11    94%

1 file skipped due to complete coverage.

============================= slowest 10 durations =============================
20.31s call     tests/test_main.py::test_retrieve_stratified_valid_numbers
14.28s call     tests/test_main.py::test_retrieve_valid_id_numbers
0.14s call     tests/test_backend.py::TestSyncIO::test_run_awk
0.05s call     tests/test_main.py::test_root

(6 durations < 0.005s hidden.  Use -vv to show these durations.)
======================== 16 passed, 1 warning in 35.79s ========================
```

The slowest endpoints are `retrieve_valid_id_numbers` and `retrieve_stratified_valid_numbers` with response times of 9.88s and 15.29s respectively.