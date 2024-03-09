import unittest

from app.functions import split, is_odd


class TestFunctions(unittest.TestCase):

    
    def test_split(self):
        """
        Test the split function for:
         - Correctness of the output
         - Exception handling
        """
        self.assertEqual(split(12345678901), {'birthday': '123456', 'person_number': '78901'})
        self.assertRaises(Exception, split, '12345678901')
        self.assertRaises(Exception, split, 12345678901.0)
    
    def test_is_odd(self):
        self.assertTrue(is_odd(3))
        self.assertFalse(is_odd(4))
        self.assertRaises(Exception, is_odd, '3')
        self.assertRaises(Exception, is_odd, 3.0)

if __name__ == '__main__':
    unittest.main()