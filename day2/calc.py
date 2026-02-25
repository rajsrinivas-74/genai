"""Calculator utility functions with input validation and exception handling."""

import math
from numbers import Real


def _validate_number(value: Real, name: str) -> None:
	"""Validate that the provided value is a real number (int or float).

	Args:
		value: Value to validate.
		name: Parameter name for clear error messages.

	Raises:
		TypeError: If value is not an int or float (excluding bool).
		ValueError: If value is NaN or infinity.
	"""
	# Reject booleans even though bool is a subclass of int.
	if isinstance(value, bool) or not isinstance(value, Real):
		raise TypeError(f"{name} must be a real number (int or float).")

	# Reject NaN and infinity to keep arithmetic safe and deterministic.
	if isinstance(value, float) and not math.isfinite(value):
		raise ValueError(f"{name} must be a finite number.")


def addition(a: Real, b: Real) -> float:
	"""Return the sum of two numbers."""
	_validate_number(a, "a")
	_validate_number(b, "b")
	return float(a + b)


def subtraction(a: Real, b: Real) -> float:
	"""Return the difference of two numbers."""
	_validate_number(a, "a")
	_validate_number(b, "b")
	return float(a - b)


def multiplication(a: Real, b: Real) -> float:
	"""Return the product of two numbers."""
	_validate_number(a, "a")
	_validate_number(b, "b")
	return float(a * b)


def division(a: Real, b: Real) -> float:
	"""Return the quotient of two numbers.

	Raises:
		ZeroDivisionError: If b is zero.
	"""
	_validate_number(a, "a")
	_validate_number(b, "b")

	if b == 0:
		raise ZeroDivisionError("Cannot divide by zero.")

	return float(a / b)


def square_root(value: Real) -> float:
	"""Return the square root of a non-negative number.

	Raises:
		ValueError: If value is negative.
	"""
	_validate_number(value, "value")

	if value < 0:
		raise ValueError("Cannot calculate square root of a negative number.")

	return float(math.sqrt(value))
