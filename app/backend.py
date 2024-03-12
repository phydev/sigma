"""
This file contains helper functions used in the API.
"""

from typing import Type, Dict, Union
from datetime import date
import asyncio

# for custom logging
from starlette.middleware.base import (
    BaseHTTPMiddleware,
    RequestResponseEndpoint)
from starlette.requests import Request
from starlette.responses import Response
import time
import logging


def validate_date(year: str, month: str, day: str) -> bool:
    """
    This function checks if the input date is valid
    according to the Gregorian calendar rules.
    :param year: year
    :param month: month
    :param day: day
    :return: True if the date is valid, False otherwise
    """
    day = int(day)
    month = int(month)
    year = int(year)

    if day > 31 or month > 12:
        return False
    elif month in [4, 6, 9, 11] and day > 30:
        return False
    elif month == 2 and day > 29:
        return False
    elif month == 2 and day > 28 and year % 4 != 0:
        return False
    elif year * day * month < 0:
        return False
    else:
        return True


def split(id_number: str) -> Dict[str, Union[Type[date], str]]:
    """
    This function splits the Norwegian ID number into two numbers
    the birthday (first 6 numbers) and the person number (last 5 numbers)

    :param id_number: 11 digits Nowegian id number
    :return splitted_id_number: a dictionary containing the
    birthday and person number

    """

    # test if id_number is provided as string

    if type(id_number) is not str:
        raise TypeError("The input must be an integer encoded as string!")

    person_number = id_number[6:]

    # check in which century the person was born
    # and add the first two digits of the year
    if int(person_number[0]) <= 4:
        birth_year = "19" + id_number[4:6]
    else:
        birth_year = "20" + id_number[4:6]

    # slice the birthday and save it as a date object
    # with the format year-month-day

    if validate_date(birth_year, id_number[2:4], id_number[:2]):
        birthday = date(int(birth_year),
                        int(id_number[2:4]),
                        int(id_number[:2])
                        )
    else:
        birthday = date(3000, 12, 25)

    # return the splitted numbers as a dictionary
    splitted_id_number = {"birthday": birthday, "person_number": person_number}

    return splitted_id_number


def is_odd(number: int) -> bool:
    """
    This function checks if a number is odd or not

    :param number: an integer
    :return: True if the number is odd, False otherwise
    """

    if type(number) is not int:
        raise TypeError(
            "The input must be an integer! \
                        Oddness is only defined for integers."
        )

    return number % 2 != 0


def transform_to_list(id_number: str) -> list:
    """
    This function transforms the input number into a list of integers
    """

    return [int(digit) for digit in str(id_number)]


def dot_product(a: int, b: int) -> int:
    """
    This function implements the element-wise multiplication of two lists.
    We implemented this function only to keep the number of dependeciess low.
    However, if high performance is needed, consider using numpy.

    :param a: a list of numbers
    :param b: a list of numbers
    :return: the dot product of a and b
    """

    if len(a) != len(b):
        raise Exception("The lists must have the same length!")

    return sum([a[i] * b[i] for i in range(len(a))])


def is_valid_id_number(id_number: str) -> bool:
    """
    This function checks if the input is a valid Norwegian ID number.
    We will use conditionally defined return calls, which can speed up
    the function avoiding unnecessary checks.
    :param id_number: 11 digits Norwegian id number
    :return: True if the number is valid, False otherwise
    """
    control_vector1 = [3, 7, 6, 1, 8, 9, 4, 5, 2, 1]
    control_vector2 = [5, 4, 3, 2, 7, 6, 5, 4, 3, 2, 1]

    if type(id_number) is not str:
        raise TypeError("The input must be an integer encoded as string!")

    if not id_number.isdigit():
        return False

    id_number_list = transform_to_list(id_number)

    if len(id_number_list) != 11:
        return False
    else:
        control_number_1 = dot_product(id_number_list[:10], control_vector1)
        control_number_2 = dot_product(id_number_list, control_vector2)

    if control_number_1 % 11 != 0:
        return False
    elif control_number_2 % 11 != 0:
        return False
    elif get_age_from(id_number) is False:
        return False
    else:
        return True


def get_gender_from(id_number: str) -> str:
    """
    This function returns the gender based on the id_number
    :param id_number: 11 digits Norwegian id number
    :return: gender of the person
    """

    if is_odd(int(id_number[8])):
        return "male"
    else:
        return "female"


def get_age_from(id_number: str) -> int:
    """
    This function returns the age of a person given their id number
    :param id_number: 11 digits Norwegian id number.
    :return: the age of the person
    """

    splitted_id = split(id_number)
    birthday = splitted_id["birthday"]
    today = date.today()
    age = today.year - birthday.year
    # Unfortunately the datetime module does not have a
    # method to calculate the age directly, so we need to
    # check if a full year has not occurred yet
    if (today.month, today.day) < (birthday.month, birthday.day):
        age -= 1

    if age < 0:
        return False
    else:
        return age


async def run_awk(filename: str, id_number: str) -> list[str]:
    """
    This function runs the awk command to search for an entry in a
    data file and returns the line number of the entry.
    We define this function as asyncronous to avoid blocking
    the event loop.
    :param filename: the name of the file to search
    :param id_number: the id_number to search for
    :return line_number: the line number of the entry
    """

    cmd = f"awk '/{id_number}/ {{print NR}}' {filename}"
    process = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )

    stdout, stderr = await process.communicate()

    if stderr:
        raise RuntimeError(f"Error executing awk: {stderr.decode()}")

    result = stdout.decode("utf-8")

    line_numbers = result.strip().split("\n") if result else []

    return line_numbers


def stratified_valid_numbers(filename: str) -> dict:
    """
    This function returns the number of valid id numbers
    stratified by gender and age groups.
    """

    valid_numbers = {
        "male": {"0-19": 0, "20-64": 0, ">=65": 0},
        "female": {"0-19": 0, "20-64": 0, ">=65": 0},
    }

    with open(filename, "r") as file:

        for line in file:
            # remove spaces at the begining and end
            clean_line = line.strip()

            # check if it is a valid number
            is_valid = is_valid_id_number(clean_line)

            if is_valid:

                # retrieve gender and age
                gender = get_gender_from(clean_line)
                age = get_age_from(clean_line)

                # stratify the age groups
                if age < 20:
                    valid_numbers[gender]["0-19"] += 1
                elif age < 65:
                    valid_numbers[gender]["20-64"] += 1
                else:
                    valid_numbers[gender][">=65"] += 1

    return valid_numbers


class TimingMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.logger = logging.getLogger("uvicorn.error")

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        self.logger.info(
            f"{request.method} {request.url} - \
                {response.status_code}: \
                    Response time: {process_time:.5f}s"
        )
        return response
