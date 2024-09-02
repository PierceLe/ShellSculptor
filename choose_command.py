"""
choose_command.py

This module provides a factory function for creating command objects
based on the user's input. The `command_factory` function returns
an appropriate command object that can be executed.

Functions:
    - command_factory(command): Returns an instance of a command class
      corresponding to the input command string.
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
    Creates and returns the appropriate command object based on the input command string.

    The `command_factory` function analyzes the first word of the input command string
    to determine which command class to instantiate. It returns an instance of the
    corresponding command class, which can then be executed.

    Args:
        command (str): The full command string input by the user.

    Returns:
        Command: An instance of a subclass of `Command` corresponding to the input command.
                 For unrecognized commands, an `ExecuteCommand` object is returned to handle
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
