import unittest

from app.backend import (
    split,
    is_odd,
    get_gender_from,
    get_age_from,
    transform_to_list,
    dot_product,
    is_valid_id_number,
    run_awk,
    stratified_valid_numbers,
)
from datetime import date


class TestFunctions(unittest.TestCase):

    def __init__(self, *args, **kwargs):

        super(TestFunctions, self).__init__(*args, **kwargs)

        self.valid_ids = ["26018835419", "02068503429"]
        self.not_valid_ids = ["30108938901", "Madalena Morgado", "1234"]
        self.odd_numbers = [1, 3, 5, 7, 9, 11]
        self.even_numbers = [2, 4, 6, 8, 10, 12]

        self.id_and_gender = {
            "id_number": [
                "26075534089",
                "18047734189",
                "16105634289",
                "05109534389",
                "01014434489",
            ],
            "gender": ["female", "male", "female", "male", "female"],
        }

        self.stratification = {
            "male": {"0-19": 0, "20-64": 0, ">=65": 0},
            "female": {"0-19": 0, "20-64": 0, ">=65": 0},
        }

    def test_split(self):
        """
        Test the split function for:
         - Correctness of the output
         - Exception handling
        """
        self.assertEqual(
            split("07105648901"),
            {"birthday": date(1956, 10, 7), "person_number": "48901"},
        )
        self.assertRaises(TypeError, split, 12345678901)

    def test_is_odd(self):
        """
        Test the odd function with a list of odd numbers
        and a list of even numbers.
        - Test TypeError handling.
        """
        for odd_number in self.odd_numbers:
            self.assertTrue(is_odd(odd_number))

        for even_number in self.even_numbers:
            self.assertFalse(is_odd(even_number))

        self.assertRaises(TypeError, is_odd, "3")
        self.assertRaises(TypeError, is_odd, 3.0)

    def test_get_gender_from(self):
        """
        Test the get_gender_from function with a dictionary
        of id numbers and their respective gender.
        """
        for n, case in enumerate(self.id_and_gender["id_number"]):
            self.assertEqual(
                get_gender_from(self.id_and_gender["id_number"][n]),
                self.id_and_gender["gender"][n],
            )

    def test_get_age_from(self):
        """
        Test if the get_age_from function returns the correct age
        based on id numbers. Test also if the funtion returns false
        when the age is a negative value.
        """

        correct_age = date.today().year - 1989

        self.assertEqual(get_age_from("01018938901"), correct_age)
        self.assertEqual(get_age_from("01018998901"), False)

    def test_transform_tolist(self):
        """
        test the transform_to_list function which
        converts a string into a list of digits.
        """
        self.assertEqual(
            transform_to_list("12345678901"), [1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1]
        )

    def test_dot_product(self):
        """
        test if the function dot_ product performs
        the vectorial product of two lists correctly.
        """
        self.assertEqual(dot_product([1, 2, 3], [1, 2, 3]), 14)
        self.assertRaises(Exception, dot_product, [1, 2, 3], [1, 2, 3, 4])

    def test_is_valid_id_number(self):
        """
        Test if the function is_valid_id_number returns True
        for a list of valid id numbers.
        """
        for valid_id in self.valid_ids:
            self.assertTrue(is_valid_id_number(valid_id))

    def test_is_not_valid_id_number(self):
        """
        test if the function is_valid_id_number returns False
        for a list of invalid id numbers.
        """
        for invalid_id in self.not_valid_ids:
            self.assertFalse(is_valid_id_number(invalid_id))

    def test_stratified_valid_numbers(self):
        """
        Test if the function stratified_valid_numbers returns
        the correct number of valid id numbers for each age group.
        """

        response = stratified_valid_numbers(filename="data/test_data.txt")

        self.assertEqual(response.keys(), self.stratification.keys())


class TestSyncIO(unittest.IsolatedAsyncioTestCase):

    async def test_run_awk(self):

        response = await run_awk("data/test_data.txt", "03025600125")
        self.assertEqual(response, ["5", "10"])


if __name__ == "__main__":
    unittest.main()
