"""
command.py

Defines the abstract base class 'Command', serves as a blueprint for the creation
of shell command classes. Stores a command string and require subclasses to implement
a 'execute' method which defines behavior of the command when executed.

Classes:
    - Command: An abstract base class for defining and executing shell commands.
"""


from abc import ABC, abstractmethod


class Command(ABC):
    """
    An abstract base class for defining shell commands.

    A blueprint for creating shell commands. Requires the implementation of
    the 'execute' method in any subclass that inherits from it. The class stores
    the command string and provides a property for access.

    Args:
        command (str): The command string to be stored and executed by subclasses.

    Attributes:
        _command (str): A protected attribute, holds the command string.

    Methods:
        get_command: Returns the stored command string.
        execute: An abstract method that must be implemented by subclasses,
                 define the execution logic of the command.
    """
    def __init__(self, command: str):
        """
        Initializes the Command object with the command string.

        Args:
            command (str): The command string to be stored.
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
        behavior when it is executed.

        Raises:
            NotImplementedError: If the method is not implemented in the subclass.
        """
