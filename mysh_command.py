"""
command.py

This module defines the abstract base class `Command`, which serves as a
blueprint for creating shell command classes. The `Command` class stores a
command string and requires subclasses to implement the `execute` method,
which defines the behavior of the command when it is executed.

Classes:
    - Command: An abstract base class for defining and executing shell commands.
"""


from abc import ABC, abstractmethod


class Command(ABC):
    """
    An abstract base class for defining shell commands.

    This class serves as a blueprint for creating various shell commands.
    It requires the implementation of the `execute` method in any subclass
    that inherits from this class. The `Command` class stores the command
    string and provides a property to access it.

    Args:
        command (str): The command string to be stored and executed by the subclass.

    Attributes:
        _command (str): A protected attribute that holds the command string.

    Methods:
        get_command: A property that returns the stored command string.
        execute: An abstract method that must be implemented by subclasses
                 to define the execution logic of the command.
    """
    def __init__(self, command: str):
        """
        Initializes the Command object with the provided command string.

        Args:
            command (str): The command string to be stored in the object.
        """
        self._command = command

    @property
    def get_command(self) -> str:
        """
        Returns the command string stored in the Command object.

        Returns:
            str: The command string.
        """
        return self._command

    @abstractmethod
    def execute(self) -> None:
        """
        Executes the command.

        This method must be implemented by subclasses to define the specific
        behavior of the command when it is executed.

        Raises:
            NotImplementedError: If the method is not implemented in the subclass.
        """
