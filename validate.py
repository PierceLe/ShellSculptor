"""
This module provides utility functions for validating shell variable names,
flags, exit codes, and command options.

Functions:
- valid_variable_name(variable_name): Validates whether a string is a valid shell variable name.
- is_flag(argument): Checks if a string is a valid flag.
- valid_exit_code(exit_code): Validates whether a given value can be used as an exit code.
- invalid_option_pwd(options): Identifies invalid options for the `pwd` command.
"""

import re

BUILTIN_COMMANDS: list = ["cd", "pwd", "exit", "var", "which"]


def valid_variable_name(variable_name: str) -> bool:
    """
    Checks if a given variable name is valid according to shell naming conventions.

    A valid variable name can only contain alphanumeric characters and underscores.

    Args:
        variable_name (str): The name of the variable to validate.

    Returns:
        bool: True if the variable name is valid, False otherwise.
    """
    pattern = r'^[A-Za-z0-9_]+$'
    return bool(re.match(pattern, variable_name))


def is_flag(argument: str) -> bool:
    """
    Determines if the given argument is a valid flag.

    A valid flag starts with a dash followed by alphabetic characters.

    Args:
        argument (str): The argument to check.

    Returns:
        bool: True if the argument is a valid flag, False otherwise.
    """
    pattern = r"^-([a-zA-Z]+)$"
    return bool(re.match(pattern, argument))


def valid_exit_code(exit_code) -> bool:
    """
    Checks if the provided exit code is a valid integer.

    Args:
        exit_code: The exit code to validate, which can be any data type.

    Returns:
        bool: True if the exit code can be converted to an integer, False otherwise.
    """
    try:
        int(exit_code)
    except ValueError:
        return False
    return True


def invalid_option_pwd(options: list) -> str:
    """
    Identifies any invalid options passed to the `pwd` command.

    The only valid option for `pwd` is 'P'. If any other option is found,
    it will be returned.

    Args:
        options (list): A list of option strings.

    Returns:
        str: The first invalid option found, or an empty string if all options are valid.
    """
    for option in options:
        if option != "P":
            return option
    return ""


def is_builtin_command(command: str) -> bool:
    """
    Checks if the given command is a builtin command.
    """
    return command in BUILTIN_COMMANDS
