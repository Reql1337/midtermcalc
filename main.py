
# ==============================================================================
# IMPORTING NECESSARY MODULES
# ==============================================================================
import logging
import pdb
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List 


# Configure the logging settings for the application.
# Logging is crucial for tracking events and diagnosing issues in applications.
logging.basicConfig(
    filename='calculator.log',  # Specifies the file to write log messages to.
    level=logging.DEBUG,  # Sets the logging level to DEBUG; captures all levels (DEBUG, INFO, WARNING, ERROR, CRITICAL).
    format='%(asctime)s - %(levelname)s - %(message)s'  # Defines the format of the log messages.
    # Format placeholders:
    # %(asctime)s - Timestamp of the log entry.
    # %(levelname)s - Severity level of the log message.
    # %(message)s - The actual log message.
)

class TemplateOperation(ABC):
    """
    Abstract base class representing a mathematical operation using the Template Method pattern.
    - Inherits from ABC to make it an abstract base class.
    - The Template Method Pattern defines the steps of an algorithm.
    """
    def calculate(self, a: float, b: float) -> float:
        """
        Template method that defines the structure for performing an operation.
        Steps:
        1. Validate inputs.
        2. Execute the operation.
        3. Log the result.
        """
        self.validate_inputs(a, b)  # Step 1: Validate the inputs.
        result = self.execute(a, b)  # Step 2: Perform the specific operation.
        self.log_result(a, b, result)  # Step 3: Log the operation and the result.
        return result  # Return the result of the operation.

    def validate_inputs(self, a: float, b: float):
        """
        Common validation method to ensure inputs are numbers.
        Raises a ValueError if inputs are not numeric types.
        """
        if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
            logging.error(f"Invalid input: {a}, {b} (Inputs must be numbers)")  # Log an error message.
            raise ValueError("Both inputs must be numbers.")  # Raise an exception.

    @abstractmethod
    def execute(self, a: float, b: float) -> float:
        """
        Abstract method to perform the specific operation.
        Must be implemented by subclasses.
        """
        pass  # This method will be overridden in child classes.

    def log_result(self, a: float, b: float, result: float):
        """
        Logs the result of the calculation.
        """
        logging.info(f"Operation performed: {a} and {b} -> Result: {result}")  # Log an informational message.


class Addition(TemplateOperation):
    """
    Class to represent the addition operation.
    Inherits from TemplateOperation.
    """
    def execute(self, a: float, b: float) -> float:
        """
        Returns the sum of two numbers.
        """
        return a + b  # Perform addition.

class Subtraction(TemplateOperation):
    """
    Class to represent the subtraction operation.
    Inherits from TemplateOperation.
    """
    def execute(self, a: float, b: float) -> float:
        """
        Returns the difference between two numbers.
        """
        return a - b  # Perform subtraction.

class Multiplication(TemplateOperation):
    """
    Class to represent the multiplication operation.
    Inherits from TemplateOperation.
    """
    def execute(self, a: float, b: float) -> float:
        """
        Returns the product of two numbers.
        """
        return a * b  # Perform multiplication.

class Division(TemplateOperation):
    """
    Class to represent the division operation.
    Inherits from TemplateOperation.
    """
    def execute(self, a: float, b: float) -> float:
        """
        Returns the quotient of two numbers.
        Raises a ValueError if attempting to divide by zero.
        """
        if b == 0:
            logging.error("Attempted to divide by zero.")  # Log an error message.
            raise ValueError("Division by zero is not allowed.")  # Raise an exception.
        return a / b  # Perform division.

class OperationFactory:
    """
    Factory class to create instances of operations based on the operation type.
    Implements the Factory Pattern.
    """
    @staticmethod
    def create_operation(operation: str) -> TemplateOperation:
        """
        Returns an instance of the appropriate Operation subclass based on the operation string.
        Parameters:
        - operation (str): The operation name (e.g., 'add', 'subtract').
        """
        # Dictionary mapping operation names to their corresponding class instances.
        operations_map = {
            "add": Addition(),
            "subtract": Subtraction(),
            "multiply": Multiplication(),
            "divide": Division(),
        }
        # Log the operation creation request at DEBUG level.
        logging.debug(f"Creating operation for: {operation}")
        # Retrieve the operation instance from the map.
        return operations_map.get(operation.lower())  # Returns None if the key is not found.
class HistoryObserver:
    """
    Observer that gets notified whenever a new calculation is added to history.
    Implements the Observer Pattern.
    """
    def update(self, calculation):
        """
        Called when a new calculation is added to the history.
        Parameters:
        - calculation (Calculation): The calculation object that was added.
        """
        # Log the notification at INFO level.
        logging.info(f"Observer: New calculation added -> {calculation}")

class CalculatorWithObserver:
    """
    Calculator class with observer support for tracking calculation history.
    Maintains a list of observers and notifies them of changes.
    """
    def __init__(self):
        self._history: List[Calculation] = []  # List to store calculation history.
        self._observers: List[HistoryObserver] = []  # List of observers.

    def add_observer(self, observer: HistoryObserver):
        """
        Adds an observer to be notified when history is updated.
        Parameters:
        - observer (HistoryObserver): The observer to add.
        """
        self._observers.append(observer)  # Add the observer to the list.
        logging.debug(f"Observer added: {observer}")  # Log the addition.

    def notify_observers(self, calculation):
        """
        Notifies all observers when a new calculation is added.
        Parameters:
        - calculation (Calculation): The calculation object that was added.
        """
        for observer in self._observers:
            observer.update(calculation)  # Call the update method on the observer.
            logging.debug(f"Notified observer about: {calculation}")  # Log the notification.

    def perform_operation(self, operation: TemplateOperation, a: float, b: float):
        """
        Performs the operation, stores it in history, and notifies observers.
        Parameters:
        - operation (TemplateOperation): The operation to perform.
        - a (float): The first operand.
        - b (float): The second operand.
        Returns:
        - The result of the operation.
        """
        calculation = Calculation(operation, a, b)  # Create a new Calculation object.
        self._history.append(calculation)  # Add the calculation to the history.
        self.notify_observers(calculation)  # Notify observers of the new calculation.
        logging.debug(f"Performed operation: {calculation}")  # Log the operation.
        return operation.calculate(a, b)  # Execute the calculation and return the result.
class SingletonCalculator:
    """
    A calculator using the Singleton pattern to ensure only one instance exists.
    """
    _instance = None  # Class variable to hold the singleton instance.

    def __new__(cls):
        """
        Overrides the __new__ method to control the creation of a new instance.
        Ensures that only one instance is created.
        """
        if cls._instance is None:
            cls._instance = super(SingletonCalculator, cls).__new__(cls)  # Call the superclass __new__ method.
            cls._history = []  # Initialize the shared history.
            logging.info("SingletonCalculator instance created.")  # Log the creation.
        return cls._instance  # Return the singleton instance.

    def perform_operation(self, operation: TemplateOperation, a: float, b: float) -> float:
        """
        Performs the given operation and stores the calculation in history.
        Parameters:
        - operation (TemplateOperation): The operation to perform.
        - a (float): The first operand.
        - b (float): The second operand.
        Returns:
        - The result of the operation.
        """
        calculation = Calculation(operation, a, b)  # Create a new Calculation object.
        self._history.append(calculation)  # Add the calculation to the shared history.
        logging.debug(f"SingletonCalculator: Performed operation -> {calculation}")  # Log the operation.
        return operation.calculate(a, b)  # Execute the calculation and return the result.

    def get_history(self):
        """
        Returns the history of calculations.
        Includes a breakpoint for debugging using pdb.
        """
       # pdb.set_trace()  # Pause execution here for debugging.
        return self._history  # Return the shared history list.


@dataclass  # Decorator to automatically generate special methods like __init__.
class Calculation:
    """
    Represents a single calculation using the Strategy Pattern.
    Holds the operation (strategy) and operands.
    """
    operation: TemplateOperation  # The operation to execute (strategy).
    operand1: float  # The first operand.
    operand2: float  # The second operand.

    def __repr__(self) -> str:
        """
        Official string representation of the Calculation object.
        Used for debugging and logging.
        """
        return f"Calculation({self.operand1}, {self.operation.__class__.__name__.lower()}, {self.operand2})"

    def __str__(self) -> str:
        """
        User-friendly string representation of the calculation and result.
        """
        result = self.operation.calculate(self.operand1, self.operand2)  # Perform the calculation.
        return f"{self.operand1} {self.operation.__class__.__name__.lower()} {self.operand2} = {result}"


def calculator():
    """
    Interactive REPL (Read-Eval-Print Loop) for performing calculator operations.
    Provides a command-line interface for users to interact with the calculator.
    """
    import pdb  # Import pdb module for debugging.

    # Create an instance of the calculator with observer support.
    calc = CalculatorWithObserver()

    # Create an observer to monitor calculation history.
    observer = HistoryObserver()

    # Add the observer to the calculator's list of observers.
    calc.add_observer(observer)

    # Display a welcome message and instructions.
    print("Welcome to the OOP Calculator! Type 'help' for available commands.")

    # Start the REPL loop.
    while True:
        # Prompt the user for input.
        user_input = input("Enter an operation and two numbers, or a command: ")

        # Handle the 'help' command.
        if user_input.lower() == "help":
            print("\nAvailable commands:")
            print("  add <num1> <num2>       : Add two numbers.")
            print("  subtract <num1> <num2>  : Subtract the second number from the first.")
            print("  multiply <num1> <num2>  : Multiply two numbers.")
            print("  divide <num1> <num2>    : Divide the first number by the second.")
            print("  list                    : Show the calculation history.")
            print("  clear                   : Clear the calculation history.")
            print("  exit                    : Exit the calculator.\n")
            continue  # Return to the start of the loop.

        # Handle the 'exit' command.
        if user_input.lower() == "exit":
            print("Exiting calculator...")
            break  # Exit the loop and end the program.

        # Handle the 'list' command to display calculation history.
        if user_input.lower() == "list":
            if not calc._history:
                print("No calculations in history.")
            else:
                for calc_item in calc._history:
                    print(calc_item)  # Calls __str__ method of Calculation.
            continue  # Return to the start of the loop.

        # Handle the 'clear' command to clear the history.
        if user_input.lower() == "clear":
            calc._history.clear()  # Clear the history list.
            logging.info("History cleared.")  # Log the action.
            print("History cleared.")
            continue  # Return to the start of the loop.

        # Attempt to parse and execute the user's command.
        try:
            # Set a breakpoint for debugging.
            # pdb.set_trace()  # Execution will pause here, allowing inspection of variables.

            # Split the user input into components.
            operation_str, num1_str, num2_str = user_input.split()  # May raise ValueError.

            # Convert the operand strings to float.
            num1, num2 = float(num1_str), float(num2_str)  # May raise ValueError.

            # Use the factory to create the appropriate operation object.
            operation = OperationFactory.create_operation(operation_str)

            if operation:
                # Perform the operation using the calculator.
                result = calc.perform_operation(operation, num1, num2)
                # Display the result to the user.
                print(f"Result: {result}")
            else:
                # Handle unknown operation names.
                print(f"Unknown operation '{operation_str}'. Type 'help' for available commands.")

        except ValueError as e:
            # Handle errors such as incorrect input format or invalid numbers.
            logging.error(f"Invalid input or error: {e}")  # Log the error.
            print("Invalid input. Please enter a valid operation and two numbers. Type 'help' for instructions.")



if __name__ == "__main__":
    # This block ensures that the calculator runs only when the script is executed directly.
    # It will not run if the script is imported as a module.
    calculator()  # Call the main calculator function to start the REPL.
