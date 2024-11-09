""" app/calculator.py """

from app.operations import addition, subtraction, multiplication, division

def calculator():
    """Basic REPL calculator that performs addition, subtraction, multiplication, and division."""
    print("Welcome to the calculator REPL! Type 'exit' to quit.")
    
    while True:
        user_input = input("Enter an operation (add, subtract, multiply, divide) and two numbers, or 'exit' to quit: ")

        if user_input.lower() == "exit":
            print("Exiting calculator...")
            break

        try:
            # Split user input into components
            operation, num1, num2 = user_input.split()
            num1, num2 = float(num1), float(num2)
        except ValueError:
            print("Invalid input. Please follow the format: <operation> <num1> <num2>")
            continue

        # Perform the corresponding operation
        if operation == "add":
            result = addition(num1, num2)
        elif operation == "subtract":
            result = subtraction(num1, num2)
        elif operation == "multiply":
            result = multiplication(num1, num2)
        elif operation == "divide":
            try:
                result = division(num1, num2)
            except ValueError as e:
                print(e)
                continue
        else:
            print(f"Unknown operation '{operation}'. Supported operations: add, subtract, multiply, divide.")
            continue

        print(f"Result: {result}")
