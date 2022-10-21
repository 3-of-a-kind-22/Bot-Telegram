import unittest
from cows_and_bulls import filter_users_number

class MyTestCase(unittest.TestCase):
    def test_filter_users_number(self):
        # Arrange
        t = [1234, 12345, "qw", 1]
        expected_results = [True, False, False, False]
        for i in range(4):
            number = t[i]
            expected_result = expected_results[i]
            result = filter_users_number(number)
            self.assertEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()
