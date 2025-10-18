from abc import ABC, abstractmethod
from typing import Union

class Operation(ABC):
    """Abstract base class for arithmetic operations."""
    @abstractmethod
    def execute(self, a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
        pass

class Addition(Operation):
    """Performs addition."""
    def execute(self, a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
        return a + b

class Subtraction(Operation):
    """Performs subtraction."""
    def execute(self, a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
        return a - b

class Multiplication(Operation):
    """Performs multiplication."""
    def execute(self, a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
        return a * b

class Division(Operation):
    """Performs division."""
    def execute(self, a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
        if b == 0:
            raise ZeroDivisionError("Cannot divide by zero.")
        return a / b

class Calculator:
    """Handles user interaction and operation execution."""
    def calculate(self, operation: Operation, a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
        """Executes the specified operation."""
        try:
            result = operation.execute(a, b)
            return result
        except ZeroDivisionError as e:
            return f"Error: {e}"
        except Exception as e:
            return f"An unexpected error occurred: {e}"

