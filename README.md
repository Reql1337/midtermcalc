# Building a Calculator with Logging/Debugging/Pandas (Midterm)

---
## Table of Contents

- VIDEO LINK: https://youtu.be/jhgqio3BLe8

1. [Introduction](#introduction)
2. [Setup Logging](#setup-logging)
3. [Operation Classes (Command and Template Method Patterns)](#operation-classes)
4. [Factory Pattern for Creating Operations](#factory-pattern)
5. [Observer Pattern for Tracking History](#observer-pattern)
6. [Singleton Pattern for Ensuring One Calculator Instance](#singleton-pattern)
7. [Strategy Pattern for Operation Selection](#strategy-pattern)
8. [Main Calculator Program (REPL Interface with Debugging)](#main-calculator-program)
9. [Conclusion](#conclusion)   

---

## Installation <a name="installation"></a>

Requirements: Python 3.8 or higher & PIP

- Clone the repository
- Install dependences using [pip install -r requirements.txt]

---

## Setup Logging <a name="setup-logging"></a>

Before diving into the code, we'll set up logging using Python's built-in `logging` module. Logging is crucial for recording events that happen during the execution of a program, which aids in debugging and monitoring.

```python
import logging

logging.basicConfig(
    filename='calculator.log',   # Log messages will be saved to this file
    level=logging.DEBUG,         # Log messages of level DEBUG and above
    format='%(asctime)s - %(levelname)s - %(message)s'  # Format of the log messages
)
```

- **Filename**: Specifies the file where logs will be stored.
- **Level**: Determines the severity levels of the logs to capture (DEBUG, INFO, WARNING, ERROR, CRITICAL).
- **Format**: Defines the format of the log messages, including timestamp, level, and message.

---

## Operation Classes (Command and Template Method Patterns) <a name="operation-classes"></a>

### Abstract Base Class: `TemplateOperation` <a name="templateoperation"></a>

We'll start by creating an abstract base class `TemplateOperation` that defines a template for all mathematical operations. This class uses the **Template Method Pattern** to outline the steps required to perform an operation.

```python
from abc import ABC, abstractmethod

class TemplateOperation(ABC):
    """
    Abstract class representing a mathematical operation using the Template Method pattern.
    """

    def calculate(self, a: float, b: float) -> float:
        """
        Template method that defines the structure for performing an operation.
        """
        self.validate_inputs(a, b)
        result = self.execute(a, b)
        self.log_result(a, b, result)
        return result

    def validate_inputs(self, a: float, b: float):
        """
        Common validation for all operations to ensure inputs are numbers.
        """
        if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
            logging.error(f"Invalid input: {a}, {b} (Inputs must be numbers)")
            raise ValueError("Both inputs must be numbers.")

    @abstractmethod
    def execute(self, a: float, b: float) -> float:
        """
        Perform the specific operation. This method will be defined by each subclass.
        """
        pass

    def log_result(self, a: float, b: float, result: float):
        """
        Log the result of the calculation.
        """
        logging.info(f"Operation performed: {a} and {b} -> Result: {result}")
```

#### Key Points:

- **Abstract Base Class**: `TemplateOperation` is an abstract class that other operation classes will inherit from.
- **Template Method Pattern**: The `calculate` method defines the steps for performing an operation:
  1. **Validate Inputs**: Ensures that the provided inputs are numbers.
  2. **Execute**: Performs the specific mathematical operation.
  3. **Log Result**: Logs the operation and its result.
- **Abstract Method**: The `execute` method is abstract, meaning each subclass must provide its own implementation.
- **Purpose**: Defines the skeleton of an algorithm in a method, deferring some steps to subclasses.
- **Implementation**: `TemplateOperation` class provides a template for operation execution.

## Factory Pattern for Creating Operations <a name="factory-pattern"></a>

The **Factory Pattern** provides a way to create objects without specifying the exact class of the object that will be created. We'll implement `OperationFactory` to create instances of our operation classes based on a string identifier.

### Class: `OperationFactory` <a name="operationfactory"></a>

```python
class OperationFactory:
    """Factory class to create instances of operations based on the operation type."""

    @staticmethod
    def create_operation(operation: str) -> TemplateOperation:
        """
        Return an instance of the appropriate Operation subclass based on the operation string.
        """
        operations_map = {
            "add": Addition(),
            "subtract": Subtraction(),
            "multiply": Multiplication(),
            "divide": Division(),
        }
        logging.debug(f"Creating operation for: {operation}")
        return operations_map.get(operation.lower())
```

#### Key Points:

- **Static Method**: `create_operation` is a static method that does not depend on an instance of the class.
- **Operations Map**: A dictionary mapping operation names to their corresponding class instances.
- **Logging**: Logs the operation request for debugging purposes.
- **Case Insensitive**: Converts the operation string to lowercase to handle different input cases.

#### Example Usage:

```python
operation = OperationFactory.create_operation("add")
result = operation.calculate(5, 3)
print(result)  # Output: 8
```

---

## Observer Pattern for Tracking History <a name="observer-pattern"></a>

The **Observer Pattern** allows an object (the subject) to notify other interested objects (observers) when its state changes. We'll use this pattern to notify observers whenever a new calculation is added to the history.

### Class: `HistoryObserver` <a name="historyobserver"></a>

```python
class HistoryObserver:
    """Observer that gets notified whenever a new calculation is added to history."""

    def update(self, calculation):
        """Called when a new calculation is added."""
        logging.info(f"Observer: New calculation added -> {calculation}")
```

#### Key Points:

- **Observer**: Listens for updates from the subject (calculator history).
- **Update Method**: Called when a new calculation is added.
- **Purpose:** Allows an object to notify other objects when its state changes.
- **Implementation:** CalculatorWithObserver notifies HistoryObserver when a new calculation is added.

### Class: `CalculatorWithObserver` <a name="calculatorwithobserver"></a>

```python
from typing import List

class CalculatorWithObserver:
    """Calculator class with observer support for tracking calculation history."""

    def __init__(self):
        self._history: List[Calculation] = []
        self._observers: List[HistoryObserver] = []

    def add_observer(self, observer: HistoryObserver):
        """Add an observer to be notified when history is updated."""
        self._observers.append(observer)
        logging.debug(f"Observer added: {observer}")

    def notify_observers(self, calculation):
        """Notify all observers when a new calculation is added."""
        for observer in self._observers:
            observer.update(calculation)
            logging.debug(f"Notified observer about: {calculation}")

    def perform_operation(self, operation: TemplateOperation, a: float, b: float):
        """Perform the operation, store it in history, and notify observers."""
        calculation = Calculation(operation, a, b)
        self._history.append(calculation)
        self.notify_observers(calculation)
        logging.debug(f"Performed operation: {calculation}")
        return operation.calculate(a, b)
```

#### Key Points:

- **Subject**: `CalculatorWithObserver` maintains a list of observers and notifies them of changes.
- **Observers List**: Keeps track of all observers to notify.
- **History**: Stores a history of all calculations performed.
- **Notification**: Calls `update` on each observer when a new calculation is added.

#### Example Usage:

```python
calc = CalculatorWithObserver()
observer = HistoryObserver()
calc.add_observer(observer)

operation = OperationFactory.create_operation("multiply")
result = calc.perform_operation(operation, 4, 5)
print(result)  # Output: 20
```

---

## Singleton Pattern for Ensuring One Calculator Instance <a name="singleton-pattern"></a>

The **Singleton Pattern** ensures that a class has only one instance and provides a global point of access to it. We'll implement a `SingletonCalculator` to ensure a single shared history across the application.

### Class: `SingletonCalculator` <a name="singletoncalculator"></a>

```python
class SingletonCalculator:
    """A calculator using the Singleton pattern to ensure only one instance exists."""
    _instance = None

    def __new__(cls):
        """Override __new__ to ensure only one instance of the class is created."""
        if cls._instance is None:
            cls._instance = super(SingletonCalculator, cls).__new__(cls)
            cls._history = []
            logging.info("SingletonCalculator instance created.")
        return cls._instance

    def perform_operation(self, operation: TemplateOperation, a: float, b: float) -> float:
        """Perform the given operation and store the calculation in history."""
        calculation = Calculation(operation, a, b)
        self._history.append(calculation)
        logging.debug(f"SingletonCalculator: Performed operation -> {calculation}")
        return operation.calculate(a, b)

    def get_history(self):
        """Return the history of calculations."""
        # Using pdb to set a breakpoint for debugging
        import pdb; pdb.set_trace()
        return self._history
```

#### Key Points:

- **Singleton Implementation**: Overrides the `__new__` method to control object creation.
- **Shared History**: All instances share the same history list.
- **Logging**: Logs the creation of the singleton instance and operations performed.
- **Debugging**: Includes a `pdb.set_trace()` call in `get_history` for debugging purposes.

#### Example Usage:

```python
singleton_calc = SingletonCalculator()
operation = OperationFactory.create_operation("subtract")
result = singleton_calc.perform_operation(operation, 10, 2)
print(result)  # Output: 8

# Accessing the shared history
history = singleton_calc.get_history()
print(history)
```

---

## Strategy Pattern for Operation Selection <a name="strategy-pattern"></a>

The **Strategy Pattern** allows selecting an algorithm at runtime. In our case, we'll encapsulate each operation as a strategy and use it interchangeably.

### Class: `Calculation` <a name="calculation"></a>

```python
from dataclasses import dataclass

@dataclass
class Calculation:
    """Represents a single calculation using the Strategy Pattern."""
    operation: TemplateOperation
    operand1: float
    operand2: float

    def __repr__(self) -> str:
        return f"Calculation({self.operand1}, {self.operation.__class__.__name__.lower()}, {self.operand2})"

    def __str__(self) -> str:
        result = self.operation.calculate(self.operand1, self.operand2)
        return f"{self.operand1} {self.operation.__class__.__name__.lower()} {self.operand2} = {result}"
```

#### Key Points:

- **Dataclass**: Simplifies the creation of classes that are primarily data containers.
- **Strategy Pattern**: The `operation` attribute holds the strategy (operation) to execute.
- **Dynamic Calculation**: Calls the `calculate` method of the provided operation.

#### Example Usage:

```python
operation = OperationFactory.create_operation("divide")
calculation = Calculation(operation, 20, 4)
print(calculation)  # Output: 20 division 4 = 5.0
```

---

## Main Calculator Program (REPL Interface with Debugging) <a name="main-calculator-program"></a>

We'll now create a Read-Eval-Print Loop (REPL) that allows users to interact with the calculator. We'll incorporate debugging using `pdb`.

### Function: `calculator()` <a name="calculator-function"></a>

```python
def calculator():
    """Interactive REPL for performing calculator operations."""
    import pdb

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
            print("  exit                    : Exit the calculator.\n")
            continue

        if user_input.lower() == "exit":
            print("Exiting calculator...")
            break

        if user_input.lower() == "list":
            if not calc._history:
                print("No calculations in history.")
            else:
                for calc_item in calc._history:
                    print(calc_item)
            continue

        if user_input.lower() == "clear":
            calc._history.clear()
            logging.info("History cleared.")
            print("History cleared.")
            continue

        try:
            pdb.set_trace()  # Debugger breakpoint

            operation_str, num1, num2 = user_input.split()
            num1, num2 = float(num1), float(num2)

            operation = OperationFactory.create_operation(operation_str)

            if operation:
                result = calc.perform_operation(operation, num1, num2)
                print(f"Result: {result}")
            else:
                print(f"Unknown operation '{operation_str}'. Type 'help' for available commands.")

        except ValueError as e:
            logging.error(f"Invalid input or error: {e}")
            print("Invalid input. Please enter a valid operation and two numbers. Type 'help' for instructions.")
```

#### Key Points:

- **REPL Loop**: Continuously prompts the user for input until they choose to exit.
- **Commands**: Supports `add`, `subtract`, `multiply`, `divide`, `list`, `clear`, and `exit`.
- **Parsing Input**: Splits the user input into operation and operands.
- **Exception Handling**: Catches `ValueError` exceptions and logs errors.
- **Debugging**: Includes a `pdb.set_trace()` call to set a breakpoint for debugging.

#### Example Usage:

- **Adding Two Numbers**:

  ```
  add 10 5
  Result: 15.0
  ```

- **Viewing History**:

  ```
  list
  10.0 addition 5.0 = 15.0
  ```

- **Clearing History**:

  ```
  clear
  History cleared.
  ```

- **Exiting the Calculator**:

  ```
  exit
  Exiting calculator...
  ```

---

## Conclusion <a name="conclusion"></a>

- In this repository there are many functionalities that are core to this assignment.
- **Command-Line Interface (REPL)**
- **Plugin System**
- **Calculation History Management with Pandas**
- **Professional Logging Practices**
- **Advanced Data Handling with Pandas**
- **Design Patterns for Scalable Architecture**

### Benefits of Using Design Patterns:

- **Reusability**: Promotes code reuse and reduces redundancy.
- **Maintainability**: Makes it easier to modify and extend code.
- **Scalability**: Facilitates the addition of new features without significant changes to existing code.
- **Readability**: Improves code organization, making it easier to understand.

---

# Quick Reference Guide

- **Add**: `add <num1> <num2>`
- **Subtract**: `subtract <num1> <num2>`
- **Multiply**: `multiply <num1> <num2>`
- **Divide**: `divide <num1> <num2>`
- **View History**: `list`
- **Clear History**: `clear`
- **Exit Program**: `exit`
- **Help**: `help`

---

# License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---