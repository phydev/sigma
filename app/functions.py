"""
This file contains helper functions used in the API.
"""

from typing import Dict, Union


def split(id_number: int) -> Dict[ str, Union[int, int]]:
    """
    This function splits the Norwegian ID number into two numbers
    the birthday (first 6 numbers) and the person number (last 5 numbers)

    :param id_number: 11 digits Nowegian id number
    :return splitted_id_number: a dictionary containing the birthday and person number 
    
    """

    # test if id_number is a valid integer 

    if type(id_number) != int:
    	raise Exception("The input must be an integer!")

    # convert to string 
    id_number_str = str(id_number)

    # slice the first 6 and the last 5 numbers
    birthday = id_number_str[:6]
    person_number = id_number_str[6:]

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

    return number % 2 != 0