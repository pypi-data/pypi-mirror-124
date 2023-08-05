"""A module for basic calculator class.

The class contains 6 methods:
add, subtract, multiply, divide, take_root and reset_memory
"""

__version__ = "0.1.1"

import time


class Calculator:
    """
    A calculator class with methods for basic arithmetic calculations.

    Arithmetic methods:
    add(num_to_add)
    subtract(num_to_subtract)
    multiply(num_to_multiply)
    divide(num_to_divide_by)
    take_root(power_of_root)

    Methods for calculator's functionality:
    reset_memory(self)
    operation(operation_input)
    """

    def __init__(self):
        self.memory: float = float(0)

    def add(self, num_to_add: float) -> float:
        """public method to add to calculator's memory

        Args:
            num_to_add (float): number to add taken from user's input

        Returns:
            float: result of addition
        """
        memory: float = self.memory
        memory: float = float(memory) + float(num_to_add)
        self.memory: float = memory
        print(memory)
        return memory

    def subtract(self, num_to_subtract: float) -> float:
        """public method to subtract from calculator's memory

        Args:
            num_to_subtract (float): number to subtract taken from user's input

        Returns:
            float: result of subtraction
        """
        memory: float = self.memory
        memory: float = float(self.memory) - float(num_to_subtract)
        self.memory: float = memory
        print(memory)
        return memory

    def multiply(self, num_to_multiply_by: float) -> float:
        """public method to multiply a number in calculator's memory

        Args:
            num_to_multiply_by (float): number to multiply by
            taken from user's input

        Returns:
            float: result of multiplication
        """
        memory: float = self.memory
        memory: float = float(memory) * float(num_to_multiply_by)
        self.memory: float = memory
        print(memory)
        return memory

    def divide(self, num_to_divide_by: float) -> float:
        """public method to divide a number in calculator's memory

        Args:
            num_to_multiply_by (float): number to divide by
            taken from user's input

        Returns:
            float: result of division
        """
        try:
            memory: float = self.memory
            memory: float = round(float(memory) / float(num_to_divide_by), 4)
            self.memory: float = memory
        except ZeroDivisionError:
            print('What\'s the point of dividing something by zero?')
        print(memory)
        return memory

    def take_root(self, power_of_root: float):
        """public method to take root from a number in calculator's memory.
        Checks to validate that the root is not taken from a negative number
        as well as the root isn't to the power of 0 as such operations
        are complex math problems.

        Args:
            power_of_root (float): number indicating
            to what power the root must be

        Returns:
            [type]: result of the root
        """
        memory: float = float(self.memory)
        if memory < 0:
            return print('Negative root makes no sense. Give it another try.')
        elif power_of_root == 0:
            print('There is no realistic reason to take 0th root.')
        else:
            memory: float = round(float(memory) ** (1/float(power_of_root)), 4)
            self.memory: float = memory
            print(memory)
            return memory

    def reset_memory(self) -> float:
        """public method to reset calculator's memory back to 0

        Returns:
            float: 0 as calculator's memory
        """
        self.memory: float = 0
        memory: float = self.memory
        print('Memory reset\n0')
        return memory

    def operation(self, operation_input: str):
        """public method to call arithmetic methods of calculator
        or reset calculator's memory (indicated through user's input)

        Args:
            operation_input (str): user is asked to press the symbol
            of an operation that they want to proceed with (symbols are
            indicated every time through the 'main' method)

        Returns:
            function call based on user's input
        """
        if operation_input == '+':
            num_to_add = float(input('Number to add?\n'))
            return self.add(num_to_add)
        elif operation_input == '-':
            num_to_subtract = float(input('Number to subtract?\n'))
            return self.subtract(num_to_subtract)
        elif operation_input == '/':
            num_to_divide_by = float(input('Number to divide by?\n'))
            return self.divide(num_to_divide_by)
        elif operation_input == '*':
            num_to_multiply_by = float(input('Number to multiply by?\n'))
            return self.multiply(num_to_multiply_by)
        elif operation_input == 'R':
            power_of_root = float(input('Power of root?\n'))
            return self.take_root(power_of_root)
        elif operation_input == '0':
            return self.reset_memory()
        else:
            print('Invalid operator')


if __name__ == '__main__':
    """Initiates calculator by giving instructions and
    asks for the first input number which will be assigned to
    calculator's memory. In case user inputs 'exit' or presses
    'Ctrl+c' on their keyboard, program closes.
    """
    print('Welcome')
    time.sleep(1)
    print('This program does basic math calculations.')
    time.sleep(2)
    message = '''\
    Type \'exit\' or press \'Ctrl+c\' at any moment to close the program
    and \'0\' for operation to reset calculator\'s memory.\
    '''
    print(message)
    time.sleep(2)
    calculator = Calculator()
    num_to_operate_on: float = float(input(
        'What\'s the number to operate on?\n'))
    calculator.memory = num_to_operate_on
    while True:
        if num_to_operate_on != 'exit':
            operator = input('Operator:\n[+, -, *, /, R, 0]?\n')
        if operator == 'exit':
            break
        elif operator == 0:
            calculator.reset_memory()
        else:
            calculator.operation(operator)
            if Exception():
                continue
