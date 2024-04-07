class StackUnderflowError(Exception):
    """Exception raised when Stack is not full."""

    def __init__(self, message):
        self.message = message


class Stack:
    """Class to represent a stack."""

    def __init__(self):
        """Initialize an empty stack."""
        self.items = []

    def push(self, item):
        """Add an item to the top of the stack.

        Args:
            item: The item to be added to the stack.
        """
        self.items.append(item)

    def pop(self):
        """Remove and return the item at the top of the stack.

        Returns:
            The item at the top of the stack.

        Raises:
            StackUnderflowError: If the stack is empty.
        """
        if not self.is_empty():
            return self.items.pop()
        raise StackUnderflowError("Insufficient number of items in stack")

    def get_last_item(self):
        """Return the item at the top of the stack without removing it.

        Returns:
            The item at the top of the stack.
        """
        if not self.is_empty():
            return self.items[-1]

    def is_empty(self):
        """Check if the stack is empty.

        Returns:
            bool: True if the stack is empty, False otherwise.
        """
        return len(self.items) == 0


class Calculator:
    """Class to perform calculations."""

    def __init__(self):
        """Initialize Calculator with an empty stack and operation mappings."""
        self.stack = Stack()
        self.operations = {
            "+": self.add,
            "-": self.subtract,
            "*": self.multiply,
            "/": self.divide,
        }
        self.other_methods = {
            "drop": self.drop,
            "swap": self.swap,
            "dup": self.dup,
            "over": self.over,
        }

    def evaluate(self, input_data):
        """Evaluate input data and return the result.

        Args:
            input_data (str): The input data to be evaluated.

        Returns:
            list: A list containing the items in the stack after evaluation.
        """
        if ":" in input_data:
            input_data = input_data.lower().split(";")
        else:
            input_data = input_data.lower().split(";")

        self.define_words(input_data)

        self.select_operations(input_data)

        return self.stack.items

    def select_operations(self, input_data):
        """Select operations to perform based on input data.

        Args:
            input_data (list): A list of strings representing input data.
        """
        for word in input_data[-1].split():
            if word.isdigit():
                self.stack.push(int(word))
            elif word in self.operations:
                self.perform_operation(word)
            elif word.lower() in self.other_methods:
                self.other_methods[word.lower()]()
            else:
                raise ValueError("Undefined operation")

    def define_words(self, input_data):
        """Define new words based on input data.

        Args:
            input_data (list): A list of strings representing input data.
        """
        for item in input_data:
            item = item.strip()
            if item.startswith(":"):
                word_definition = item.split(":")[1].strip()
                word_name, definition = word_definition.split(" ", 1)
                self.other_methods[word_name] = (
                    lambda definition=definition: self.evaluate(definition)
                )

    def perform_operation(self, operation):
        """Perform arithmetic operation on top two items of the stack.

        Args:
            operation (str): The operation to be performed.
        """
        if len(self.stack.items) < 2:
            raise StackUnderflowError("Insufficient number of items in stack")
        operand2 = self.stack.pop()
        operand1 = self.stack.pop()
        if operation == "/" and operand2 == 0:
            raise ZeroDivisionError("Division by zero")
        result = self.operations[operation](operand1, operand2)
        self.stack.push(result)

    def add(self, operand1, operand2):
        """Add two operands.

        Args:
            operand1: The first operand.
            operand2: The second operand.

        Returns:
            The result of the addition operation.
        """
        return operand1 + operand2

    def subtract(self, operand1, operand2):
        """Subtract operand2 from operand1.

        Args:
            operand1: The first operand.
            operand2: The second operand.

        Returns:
            The result of the subtraction operation.
        """
        return operand1 - operand2

    def multiply(self, operand1, operand2):
        """Multiply two operands.

        Args:
            operand1: The first operand.
            operand2: The second operand.

        Returns:
            The result of the multiplication operation.
        """
        return operand1 * operand2

    def divide(self, operand1, operand2):
        """Divide operand1 by operand2.

        Args:
            operand1: The first operand.
            operand2: The second operand.

        Returns:
            The result of the division operation.
        """
        return operand1 // operand2

    def drop(self):
        """Remove the top item from the stack."""
        self.stack.pop()

    def swap(self):
        """Swap the top two items on the stack."""
        if len(self.stack.items) < 2:
            raise StackUnderflowError("Insufficient number of items in stack")
        last_item = self.stack.pop()
        new_last_item = self.stack.pop()
        self.stack.push(last_item)
        self.stack.push(new_last_item)

    def dup(self):
        """Duplicate the top item on the stack."""
        if self.stack.is_empty():
            raise StackUnderflowError("Insufficient number of items in stack")
        self.stack.push(self.stack.get_last_item())

    def over(self):
        """Copy the second item from the top of the stack."""
        if len(self.stack.items) < 2:
            raise StackUnderflowError("Insufficient number of items in stack")
        new_last_item = self.stack.items[-2]
        self.stack.push(new_last_item)


# Exemplo de uso:
calculator = Calculator()
input_data = ": DOUBLE 2 *; : TRIPLE 3 *; 4 TRIPLE DOUBLE"
# input_data = "4 4 *"
result = calculator.evaluate(input_data)
print(result)
