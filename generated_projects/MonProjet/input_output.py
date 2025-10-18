def get_input() -> tuple[str, Union[int, float], Union[int, float]]:
    """Gets user input and validates it."""
    while True:
        try:
            operation = input("Enter operation (+, -, *, /): ")
            a = float(input("Enter first operand: "))
            b = float(input("Enter second operand: "))
            return operation, a, b
        except ValueError:
            print("Invalid input. Please enter numbers for operands.")

def display_result(result: Union[int, float, str]) -> None:
    """Displays the result to the user."""
    print("Result:", result)

