"""Unit tests for calculator functions in calc.py."""

import math
import unittest

from calc import addition, subtraction, multiplication, division, square_root


class TestCalculatorFunctions(unittest.TestCase):
    """Test suite covering normal and edge/error cases."""

    def test_addition_valid(self):
        self.assertEqual(addition(2, 3), 5.0)
        self.assertEqual(addition(-2, 3), 1.0)
        self.assertAlmostEqual(addition(0.1, 0.2), 0.3, places=7)
        self.assertEqual(addition(10**12, 10**12), 2000000000000.0)

    def test_subtraction_valid(self):
        self.assertEqual(subtraction(10, 4), 6.0)
        self.assertEqual(subtraction(-5, -5), 0.0)

    def test_multiplication_valid(self):
        self.assertEqual(multiplication(4, 5), 20.0)
        self.assertEqual(multiplication(-3, 2), -6.0)
        self.assertEqual(multiplication(0, 99), 0.0)

    def test_division_valid(self):
        self.assertEqual(division(10, 2), 5.0)
        self.assertEqual(division(-9, 3), -3.0)
        self.assertEqual(division(0, 5), 0.0)

    def test_square_root_valid(self):
        self.assertEqual(square_root(25), 5.0)
        self.assertEqual(square_root(0), 0.0)
        self.assertAlmostEqual(square_root(2), math.sqrt(2), places=7)
        self.assertAlmostEqual(square_root(1e-12), 1e-6, places=12)

    def test_division_by_zero(self):
        with self.assertRaises(ZeroDivisionError):
            division(10, 0)

        # -0.0 should also be treated as zero.
        with self.assertRaises(ZeroDivisionError):
            division(10, -0.0)

    def test_square_root_negative(self):
        with self.assertRaises(ValueError):
            square_root(-1)

    def test_type_validation_errors(self):
        # Strings are invalid input.
        with self.assertRaises(TypeError):
            addition("2", 3)

        # None is invalid input.
        with self.assertRaises(TypeError):
            division(None, 2)

        # Complex numbers are not accepted (not Real).
        with self.assertRaises(TypeError):
            multiplication(1 + 2j, 3)

        # Containers are invalid input.
        with self.assertRaises(TypeError):
            subtraction([1], 2)

        # Booleans are explicitly rejected.
        with self.assertRaises(TypeError):
            subtraction(True, 1)

        with self.assertRaises(TypeError):
            multiplication(2, False)

        with self.assertRaises(TypeError):
            square_root(True)

    def test_finite_number_validation_errors(self):
        # NaN and infinity should be rejected.
        with self.assertRaises(ValueError):
            addition(float("nan"), 1)

        with self.assertRaises(ValueError):
            subtraction(1, float("nan"))

        with self.assertRaises(ValueError):
            multiplication(float("-inf"), 2)

        with self.assertRaises(ValueError):
            division(1, float("inf"))

        with self.assertRaises(ValueError):
            square_root(float("inf"))


if __name__ == "__main__":
    unittest.main()
