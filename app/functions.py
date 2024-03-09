"""
This file contains helper functions used in the API.
"""

from typing import Type, Dict, Union
from datetime import date
import asyncio

def split(id_number: str) -> Dict[ str, Union[Type[date], str]]:
    """
    This function splits the Norwegian ID number into two numbers
    the birthday (first 6 numbers) and the person number (last 5 numbers)

    :param id_number: 11 digits Nowegian id number
    :return splitted_id_number: a dictionary containing the birthday and person number 
    
    """

    # test if id_number is provided as string

    if type(id_number) != str:
        raise TypeError("The input must be an integer encoded as string!")

    person_number = id_number[6:]

    # check in which century the person was born
    # and add the first two digits of the year
    if int(person_number[0]) <=4:
        birth_year = '19' + id_number[4:6]
    else:
        birth_year = '20' + id_number[4:6]

 
    # slice the birthday and save it as a date object
    # with the format year-month-day
    birthday = date(
            int(birth_year), 
            int(id_number[2:4]), 
            int(id_number[:2])
            )

    

    # return the splitted numbers as a dictionary
    splitted_id_number = {
        'birthday': birthday, 
        'person_number': person_number
        }

    return splitted_id_number


def is_odd(number: int) -> bool:
    """
    This function checks if a number is odd or not

    :param number: an integer
    :return: True if the number is odd, False otherwise
    """

    if type(number) != int:
        raise TypeError("The input must be an integer! \
                        Oddness is only defined for integers.")

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

    if type(id_number) != str:
        raise TypeError("The input must be an integer encoded as string!")
    
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
    birthday = splitted_id['birthday']
    today = date.today()
    age = today.year - birthday.year
    # Unfortunately the datetime module does not have a 
    # method to calculate the age directly, so we need to
    # check if a full year has not occurred yet
    if (today.month, today.day) < (birthday.month, birthday.day):
        age -= 1

    if age < 0:
        raise Exception("The person has not been born yet!")
    
    return age


async def run_awk(filename: str, id_number: str) -> str:
    """
    This function runs the awk command to search for an entry in a
    data file and returns the line number of the entry.
    We define this function as asyncronous to avoid blocking the event loop.
    :param filename: the name of the file to search
    :param id_number: the id_number to search for
    """

    cmd = f'awk \'/{id_number}/ {{print NR}}\' {filename}'
    process = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )

    stdout, stderr = await process.communicate()

    if stderr:
        raise RuntimeError(f'Error executing awk: {stderr.decode()}')
    return stdout.decode('utf-8')

    
