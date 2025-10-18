from calculator import Calculator, Addition, Subtraction, Multiplication, Division
from input_output import get_input, display_result

if __name__ == "__main__":
    calculator = Calculator()
    operation_str, a, b = get_input()

    operation = None
    if operation_str == '+':
        operation = Addition()
    elif operation_str == '-':
        operation = Subtraction()
    elif operation_str == '*':
        operation = Multiplication()
    elif operation_str == '/':
        operation = Division()
    else:
        print("Invalid operation.")
        exit()

    result = calculator.calculate(operation, a, b)
    display_result(result)

