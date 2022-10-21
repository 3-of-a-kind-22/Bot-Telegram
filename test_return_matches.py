import unittest
from cows_and_bulls import return_matches

class MyTestCase(unittest.TestCase):
    def test_return_matches(self):
        # Arrange
        data1 = [1234, 1234, 5678, 4123, 1234]
        data2 = [1234, 1289, 9865, 1234, 5678]
        expected_result1 = [(4, 0), (2, 0), (0, 3), (0, 4), (0, 0)]
        for i in range(4):
            number = data1[i]
            guess = data2[i]
            expected_result = expected_result1[i]
            # Action
            result = return_matches(number, guess)
            # Asset
            self.assertEqual(result, expected_result)  # add assertion her


if __name__ == '__main__':
    unittest.main()
