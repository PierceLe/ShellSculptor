"""
Module to handle parsing for the shell.
"""
import re


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
        cmd_str: The command string we wish to split on the unquoted pipe operator ('|').

    Returns:
        A list of strings that was split on the unquoted pipe operator.
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
