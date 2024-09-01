import re


def valid_variable_name(variable_name: str) -> bool:
    pattern = r'^[A-Za-z0-9_]+$'
    return bool(re.match(pattern, variable_name))
    


def isFlag(argument: str) -> bool:
    pattern = r"^-([a-zA-Z]+)$"
    return bool(re.match(pattern, argument))
