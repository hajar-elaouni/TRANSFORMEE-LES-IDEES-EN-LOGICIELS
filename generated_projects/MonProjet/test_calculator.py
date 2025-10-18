import unittest
from calculator import Addition, Subtraction, Multiplication, Division, Calculator

class TestCalculator(unittest.TestCase):
    def setUp(self):
        self.calculator = Calculator()

    def test_addition(self):
        self.assertEqual(self.calculator.calculate(Addition(), 5, 3), 8)

    def test_subtraction(self):
        self.assertEqual(self.calculator.calculate(Subtraction(), 5, 3), 2)

    def test_multiplication(self):
        self.assertEqual(self.calculator.calculate(Multiplication(), 5, 3), 15)

    def test_division(self):
        self.assertEqual(self.calculator.calculate(Division(), 6, 2), 3.0)

    def test_division_by_zero(self):
        self.assertEqual(self.calculator.calculate(Division(), 5, 0), "Error: Cannot divide by zero.")

    def test_invalid_input(self):
        #Testing error handling for invalid input types is done within the get_input function.
        pass


if __name__ == '__main__':
    unittest.main()
