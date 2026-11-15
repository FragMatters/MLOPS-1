"""Unit tests for core arithmetic operations."""

import pytest
from arithmetic_service.core import add, subtract, multiply, divide


def test_add_positive_numbers():
    assert add(5, 3) == 8


def test_add_floats_and_negatives():
    assert pytest.approx(add(-4.5, 2.5)) == -2.0
    assert pytest.approx(add(0.1, 0.2)) == 0.3


def test_subtract_positive_numbers():
    assert subtract(10, 4) == 6


def test_subtract_resulting_negative():
    assert subtract(3, 7) == -4
    assert pytest.approx(subtract(5.5, 1.2)) == 4.3


def test_multiply_numbers():
    assert multiply(6, 7) == 42
    assert multiply(9.5, 0) == 0.0
    assert pytest.approx(multiply(-2.5, 4)) == -10.0


def test_divide_numbers():
    assert divide(20, 4) == 5.0
    assert pytest.approx(divide(7, 2)) == 3.5
    assert divide(0, 5) == 0.0


def test_divide_by_zero():
    with pytest.raises(ValueError, match="Division by zero is not allowed"):
        divide(10, 0)
