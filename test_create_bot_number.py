import unittest
from cows_and_bulls import create_bot_number

class MyTestCase(unittest.TestCase):
    def test_create_bot_number(self):
        # Arrange
        expected_result = []
        for i in range(1000,9999):
            expected_result.append(i)
        # Action
        result = create_bot_number()
        # Asset
        self.assertIn(result, expected_result)  # add assertion here


if __name__ == '__main__':
    unittest.main()
