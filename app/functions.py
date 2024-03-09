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

    if type(number) != int:
        raise Exception("The input must be an integer! \
                        Oddness is only defined for integers.")

    return number % 2 != 0

def transform_to_list(id_number: int) -> list:
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

def is_valid_id_number(id_number: int) -> bool:
    """
    This function checks if the input is a valid Norwegian ID number.
    We will use conditionally defined return calls, which can speed up
    the function avoiding unnecessary checks.
    :param id_number: 11 digits Norwegian id number
    :return: True if the number is valid, False otherwise
    """
    control_vector1 = [3, 7, 6, 1, 8, 9, 4, 5, 2, 1]
    control_vector2 = [5, 4, 3, 2, 7, 6, 5, 4, 3, 2, 1]

    if type(id_number) != int:
        return False
    else:
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

