# genai
Code Base for Gen AI Training

## Day 2 Calculator

The `day2/calc.py` module provides reusable calculator functions with:
- Input validation for numeric values
- Exception handling for invalid and edge-case inputs
- Support for common operations:
  - `addition(a, b)`
  - `subtraction(a, b)`
  - `multiplication(a, b)`
  - `division(a, b)`
  - `square_root(value)`

### Validation and Exceptions

- Raises `TypeError` for non-numeric inputs (including booleans)
- Raises `ValueError` for non-finite values (`NaN`, `inf`) and negative square root input
- Raises `ZeroDivisionError` when dividing by zero

## Usage

From the project root:

```bash
cd day2
python
```

Example:

```python
from calc import addition, division, square_root

print(addition(10, 5))      # 15.0
print(division(20, 4))      # 5.0
print(square_root(81))      # 9.0
```

## Unit Tests

The `day2/test_calc.py` file contains unit tests for all calculator functions, including edge cases and invalid data.

Run tests from project root:

```bash
cd day2
python -m unittest -v
```

This executes all tests in `test_calc.py` and reports detailed results.
