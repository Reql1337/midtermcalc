# app/operations.py

def addition(a: float, b: float) -> float:
    """Returns the sum of two numbers."""
    return a + b

def subtraction(a: float, b: float) -> float:
    """Returns the difference between two numbers."""
    return a - b

def multiplication(a: float, b: float) -> float:
    """Returns the product of two numbers."""
    return a * b

def division(a: float, b: float) -> float:
    """Returns the quotient of two numbers. Raises ValueError on division by zero."""
    if b == 0:
        raise ValueError("Division by zero is not allowed.")
    return a / b
