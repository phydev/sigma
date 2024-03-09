import unittest

from app.functions import (split, 
                           is_odd, 
                           get_gender_from,
                           get_age_from, 
                           transform_to_list,
                           dot_product,
                           is_valid_id_number
                           )
from datetime import date

class TestFunctions(unittest.TestCase):

    
    def test_split(self):
        """
        Test the split function for:
         - Correctness of the output
         - Exception handling
        """
        self.assertEqual(split('07105648901'), 
                         {'birthday': date(1956,10,7), 
                          'person_number': '48901'}
                         )
        self.assertRaises(TypeError, split, 12345678901)

 
    def test_is_odd(self):
        self.assertTrue(is_odd(3))
        self.assertFalse(is_odd(4))
        self.assertRaises(TypeError, is_odd, '3')
        self.assertRaises(TypeError, is_odd, 3.0)

    def test_get_gender_from(self):
        self.assertEqual(get_gender_from('30108934489'), "female")
        self.assertEqual(get_gender_from('30108934389'), "male")

    def test_get_age_from(self):
        self.assertEqual(get_age_from('30108938901'), 34)
        self.assertRaises(Exception, get_age_from, '30108998901')

    def test_transform_tolist(self):
        self.assertEqual(transform_to_list('12345678901'), [1,2,3,4,5,6,7,8,9,0,1])

    def test_dot_product(self):
        self.assertEqual(dot_product([1,2,3], [1,2,3]), 14)
        self.assertRaises(Exception, dot_product, [1,2,3], [1,2,3,4])

    def test_is_valid_id_number(self):
        self.assertTrue(is_valid_id_number('26018835419'))
        self.assertFalse(is_valid_id_number('30108938901'))
        self.assertTrue(is_valid_id_number('02068503429'))
        self.assertFalse(is_valid_id_number('Madalena Morgado'))
        self.assertFalse(is_valid_id_number('1234'))

if __name__ == '__main__':
    unittest.main()