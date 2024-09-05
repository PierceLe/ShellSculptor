"""
choose_command.py

Provides a factory function to create command objects based on input provided. 
Returns an appropriate executable command object.

Functions:
    - command_factory(command): return command object responding to the
    input provided.
      
"""


import parsing
import validate
from mysh_command import Command
from cd_command import Cd
from exit_command import Exit
from pwd_command import Pwd
from which_command import Which
from var_command import Var
from executing_commands import ExecuteCommand


def command_factory(command: str) -> Command:
    """
    Creates and returns the command object based on input received.

    The function reads the first word of the command string to determing
    which class to instantiate. it returns an executable instance of that class.

    Args:
        command (str): The full command input provided.

    Returns:
        Command: An instance of a subclass of `Command` based on input received.
                 If command is not recognized, an `ExecuteCommand` object is returned to handle
                 general shell commands.

    Example:
        command = "cd /home/user"
        command_obj = command_factory(command)
        command_obj.execute()  # Executes the 'cd' command
    """
    command_argument: list = parsing.split_arguments(command)
    if command_argument[0] == "var":
        return Var(command)
    if "|" in command or not validate.is_builtin_command(command_argument[0]):
        return ExecuteCommand(command)
    if command_argument[0] == "exit":
        return Exit(command)
    if command_argument[0] == "pwd":
        return Pwd(command)
    if command_argument[0] == "cd":
        return Cd(command)
    return Which(command)
