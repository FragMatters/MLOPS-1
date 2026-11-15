"""Core arithmetic computation functions."""

from typing import Union

Number = Union[int, float]


def add(a: Number, b: Number) -> Number:
    """Return the sum of two numbers (a + b)."""
    return a + b


def subtract(a: Number, b: Number) -> Number:
    """Return the difference of two numbers (a - b)."""
    return a - b


def multiply(a: Number, b: Number) -> Number:
    """Return the product of two numbers (a * b)."""
    return a * b


def divide(a: Number, b: Number) -> float:
    """Return the quotient of a divided by b.

    Raises:
        ValueError: If b == 0 (division by zero).
    """
    if b == 0:
        raise ValueError("Division by zero is not allowed")
    return a / b
