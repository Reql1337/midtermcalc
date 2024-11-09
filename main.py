import logging
import os
import pandas as pd
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List
from dotenv import load_dotenv  # Importing dotenv to read environment variables

# ============================================================================== #
# CONFIGURATION AND LOGGING
# ============================================================================== #

# Load environment variables from .env file
load_dotenv()

# Read the history file path from the environment variable
history_file = os.getenv("HISTORY_FILE", "calculator_history.csv")  # Default to 'calculator_history.csv' if not set

logging.basicConfig(
    filename='calculator.log',  # Log to a file
    level=logging.DEBUG,        # Capture all levels of logging (DEBUG and above)
    format='%(asctime)s - %(levelname)s - %(message)s'  # Log format
)

# ============================================================================== #
# CLASSES AND CALCULATOR OPERATIONS
# ============================================================================== #

class TemplateOperation(ABC):
    """
    Abstract base class representing a mathematical operation using the Template Method pattern.
    """

    def calculate(self, a: float, b: float) -> float:
        self.validate_inputs(a, b)
        result = self.execute(a, b)
        self.log_result(a, b, result)
        return result

    def validate_inputs(self, a: float, b: float):
        """
        Validates inputs to ensure they are numbers.
        """
        if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
            logging.error(f"Invalid input: {a}, {b} (Inputs must be numbers)")
            raise ValueError("Both inputs must be numbers.")

    @abstractmethod
    def execute(self, a: float, b: float) -> float:
        pass

    def log_result(self, a: float, b: float, result: float):
        """
        Logs the result of the operation.
        """
        logging.info(f"Operation performed: {a} and {b} -> Result: {result}")


class Addition(TemplateOperation):
    def execute(self, a: float, b: float) -> float:
        return a + b


class Subtraction(TemplateOperation):
    def execute(self, a: float, b: float) -> float:
        return a - b


class Multiplication(TemplateOperation):
    def execute(self, a: float, b: float) -> float:
        return a * b


class Division(TemplateOperation):
    def execute(self, a: float, b: float) -> float:
        if b == 0:
            logging.error("Attempted to divide by zero.")
            raise ValueError("Division by zero is not allowed.")
        return a / b


class OperationFactory:
    @staticmethod
    def create_operation(operation: str) -> TemplateOperation:
        operations_map = {
            "add": Addition(),
            "subtract": Subtraction(),
            "multiply": Multiplication(),
            "divide": Division(),
        }
        logging.debug(f"Creating operation for: {operation}")
        return operations_map.get(operation.lower())


class HistoryObserver:
    """
    Observer that gets notified whenever a new calculation is added to history.
    """

    def update(self, calculation):
        logging.info(f"Observer: New calculation added -> {calculation}")


@dataclass
class Calculation:
    operation: TemplateOperation
    operand1: float
    operand2: float

    def __repr__(self) -> str:
        return f"Calculation({self.operand1}, {self.operation.__class__.__name__.lower()}, {self.operand2})"

    def __str__(self) -> str:
        result = self.operation.calculate(self.operand1, self.operand2)
        return f"{self.operand1} {self.operation.__class__.__name__.lower()} {self.operand2} = {result}"


class CalculatorWithObserver:
    """
    Calculator class with observer support for tracking calculation history and CSV persistence.
    """

    def __init__(self, history_file=history_file):
        self.history_file = history_file
        self._history: List[Calculation] = self.load_history()
        self._observers: List[HistoryObserver] = []

    def add_observer(self, observer: HistoryObserver):
        self._observers.append(observer)
        logging.debug(f"Observer added: {observer}")

    def notify_observers(self, calculation):
        for observer in self._observers:
            observer.update(calculation)
            logging.debug(f"Notified observer about: {calculation}")

    def perform_operation(self, operation: TemplateOperation, a: float, b: float):
        calculation = Calculation(operation, a, b)
        self._history.append(calculation)
        self.notify_observers(calculation)
        logging.debug(f"Performed operation: {calculation}")
        self.save_history()
        return operation.calculate(a, b)

    def save_history(self):
        history_data = [
            {"Operation": str(calc.operation.__class__.__name__), "Operand1": calc.operand1, "Operand2": calc.operand2, "Result": calc.operation.calculate(calc.operand1, calc.operand2)}
            for calc in self._history
        ]
        df = pd.DataFrame(history_data)
        df.to_csv(self.history_file, index=False)
        logging.info(f"History saved to {self.history_file}")

    def load_history(self):
        if os.path.exists(self.history_file):
            df = pd.read_csv(self.history_file)
            history = [
                Calculation(OperationFactory.create_operation(row["Operation"].lower()), row["Operand1"], row["Operand2"])
                for index, row in df.iterrows()
            ]
            logging.info(f"Loaded history from {self.history_file}")
            return history
        else:
            logging.info("No history file found. Starting fresh.")
            return []

    def get_history(self):
        return self._history

    def load_history_manually(self):
        """
        Manually load history from the CSV file.
        """
        logging.info(f"Loading history manually from {self.history_file}...")
        return self.load_history()

    def save_history_manually(self):
        """
        Manually save the current history to the CSV file.
        """
        logging.info(f"Saving history manually to {self.history_file}...")
        self.save_history()


# ============================================================================== #
# REPL INTERFACE
# ============================================================================== #

def calculator():
    calc = CalculatorWithObserver()

    observer = HistoryObserver()
    calc.add_observer(observer)

    print("Welcome to the OOP Calculator! Type 'help' for available commands.")

    while True:
        user_input = input("Enter an operation and two numbers, or a command: ")

        if user_input.lower() == "help":
            print("\nAvailable commands:")
            print("  add <num1> <num2>       : Add two numbers.")
            print("  subtract <num1> <num2>  : Subtract the second number from the first.")
            print("  multiply <num1> <num2>  : Multiply two numbers.")
            print("  divide <num1> <num2>    : Divide the first number by the second.")
            print("  list                    : Show the calculation history.")
            print("  clear                   : Clear the calculation history.")
            print("  save_history            : Save the history manually.")
            print("  load_history            : Load the history manually.")
            print("  exit                    : Exit the calculator.\n")
            continue

        if user_input.lower() == "exit":
            print("Exiting calculator...")
            break

        if user_input.lower() == "list":
            if not calc.get_history():
                print("No calculations in history.")
            else:
                for calc_item in calc.get_history():
                    print(calc_item)
            continue

        if user_input.lower() == "clear":
            calc._history.clear()
            calc.save_history()
            logging.info("History cleared.")
            print("History cleared.")
            continue

        if user_input.lower() == "save_history":
            calc.save_history_manually()
            print(f"History manually saved to {calc.history_file}")
            continue

        if user_input.lower() == "load_history":
            calc.load_history_manually()
            print(f"History manually loaded from {calc.history_file}")
            continue

        try:
            operation_str, num1_str, num2_str = user_input.split()
            num1, num2 = float(num1_str), float(num2_str)
            operation = OperationFactory.create_operation(operation_str)

            if operation:
                result = calc.perform_operation(operation, num1, num2)
                print(f"Result: {result}")
            else:
                print(f"Unknown operation '{operation_str}'. Type 'help' for available commands.")

        except ValueError as e:
            logging.error(f"Invalid input or error: {e}")
            print("Invalid input. Please enter a valid operation and two numbers. Type 'help' for instructions.")


if __name__ == "__main__":
    calculator()
