"""
parsing.py

This module preprocesses user input in mysh shell before it is executed by `mysh_command`.
This module will have function to split commands by pipe operators, resolving shell variables,
which are saved into environment variables, and splitting a line into arguments using shlex.

Functions:
    - split_by_pipe_op(cmd_str): Splits a piping command into subcommands.
      This function returns a list of strings where each element is a subcommand of piping.
    - solving_shell_variable(command): Resolves shell variables in a command string,
      substituting them with their corresponding values from the environment.
      Returns the final command or False if the variable name is not valid using
      `valid_variable_name` function in validate module.
    - split_arguments(command): Splits a command string into a list of arguments,
      handling quotes and whitespace appropriately. Returns a list of split arguments
      or an empty list if an error occurs.

Internal Functions:
    - _substitute_variable(full_match, variable_name): Substitutes a shell variable
      with its value from the environment. Returns the substituted string
      and a boolean indicating whether an error occurred.
"""
import os
import sys
import re
import shlex
from typing import Union
import validate


# You are free to add functions or modify this module as you please.

_PIPE_REGEX_PATTERN = re.compile(
    # Match escaped double quotes
    r"\\\""
    # OR match escaped single quotes
    r"|\\'"
    # OR match strings in double quotes (escaped double quotes inside other quotes are OK)
    r"|\"(?:\\\"|[^\"])*\""
    # OR match strings in single quotes (escaped single quotes inside other quotes are OK)
    r"|'(?:\\'|[^'])*'"
    # OTHERWISE: match the pipe operator, and make a capture group for this
    r"|(\|)"
)
"""
Regex pattern which will perform multiple matches for escaped quotes or quoted strings,
but only contain a capture group for an unquoted pipe operator ('|').

Original regex credit to zx81 on Stack Overflow (https://stackoverflow.com/a/23667311).
"""


def split_by_pipe_op(cmd_str: str) -> list[str]:
    """
    Split a string by an unquoted pipe operator ('|').

    The logic for this function was derived from 
    https://www.rexegg.com/regex-best-trick.php#notarzan.

    >>> split_by_pipe_op("a | b")
    ['a ', ' b']
    >>> split_by_pipe_op("a | b|c")
    ['a ', ' b', 'c']
    >>> split_by_pipe_op("'a | b'")
    ["'a | b'"]
    >>> split_by_pipe_op("a '|' b")
    ["a '|' b"]
    >>> split_by_pipe_op(r"a | b 'c|d'| ef\\"|\\" g")
    ['a ', " b 'c|d'", ' ef\\\\"', '\\\\" g']
    >>> split_by_pipe_op("a|b '| c' | ")
    ['a', "b '| c' ", ' ']

    Args:
        cmd_str: The piping command.

    Returns:
        A list of subcommand.
    """
    # If you'd like, you're free to modify this function as you need.

    # Indexes which we will split the string by
    split_str_indexes = []

    for match in _PIPE_REGEX_PATTERN.finditer(cmd_str):
        if match.group(1) is not None:
            # A group exists - which is only for the last alternative
            # All other alternatives have non-capture groups, meaning they will have
            # `group(1)` return `None`
            split_str_indexes.append(match.start())

    if not split_str_indexes:
        # Nothing to split
        return [cmd_str]

    # Now, we actually split the string by the pipe operator (identified at indexes in
    # `split_str_indexes`)
    split_str = []
    prev_index = 0
    for next_index in split_str_indexes:
        # Slice string
        cmd_str_slice = cmd_str[prev_index:next_index]
        split_str.append(cmd_str_slice)

        # Update index
        prev_index = next_index + 1

    cmd_str_slice = cmd_str[prev_index:]
    split_str.append(cmd_str_slice)

    # Return string list
    return split_str


def solving_shell_variable(command: str) -> Union[bool, str]:
    """
    Resolves shell variables in a command string by substituting them with their
    corresponding values from the environment.

    This function identifies shell variables in the given command string using a
    regex pattern. For each identified variable, it attempts to substitute the
    variable with its value from the environment. If a variable name is invalid,
    an error message is printed, and the function returns `False`.

    Args:
        command (str): The command string containing shell variables to resolve.

    Returns:
        Union[bool, str]: The command string with resolved variables, or `False`
        if a syntax error occurred due to invalid variable names.
    """
    pattern = r"\\?\$\{(.*?)\}" # the pattern that match with shell variable
    error_occurred = False # boolean to check that the error occur or not

    matches = re.finditer(pattern, command)
    for match in matches:
        full_match = match.group(0)
        variable_name = match.group(1)
        replacement, error_occurred = _substitute_variable(full_match, variable_name)
        command = command.replace(full_match, replacement)

    return command if not error_occurred else False


def _substitute_variable(full_match: str, variable_name: str) -> tuple[str, bool]:
    """
    Substitutes a shell variable with its corresponding value from the environment.

    This function checks if the given shell variable is valid and not escaped.
    If the variable is valid, it retrieves its value from the environment and
    returns it along with a `False` flag indicating no error. If the variable
    is invalid or escaped, it returns an appropriate response and a `True` flag
    indicating that an error occurred.

    Args:
        full_match (str): The full string that matched the regex pattern,
                          including the shell variable.
        variable_name (str): The extracted name of the variable to be substituted.

    Returns:
        tuple[str, bool]: A tuple containing:
            - The substituted string (or an empty string if an error occurred).
            - A boolean indicating whether an error occurred (`True` if there
              was an error, `False` otherwise).
    """
    if full_match.startswith('\\$'):
        return full_match[1:], False

    if not variable_name or not validate.valid_variable_name(variable_name):
        print(
            f"mysh: syntax error: invalid characters for variable {variable_name}",
            file=sys.stderr
        )
        return "", True

    return os.environ.get(variable_name, ""), False


def split_arguments(command: str) -> list:
    """
    Splits a command string into a list of arguments, handling quotes and
    whitespace appropriately.

    This function uses the `shlex` module to split the input command string
    into a list of arguments, respecting quoted strings and escaping rules.
    It also expands user home directories if the argument starts with `~`.

    Args:
        command (str): The command string to be split into arguments.

    Returns:
        list: A list of strings representing the split arguments.
        If a `ValueError` occurs during splitting, an empty list is returned.
    """
    try:
        s = shlex.shlex(command, posix=True)
        s.escapedquotes = "'\""
        s.whitespace_split = True
        return [os.path.expanduser(arg) for arg in list(s)]
    except ValueError:
        return []
