import re


def valid_variable_name(variable_name: str) -> bool:
    pattern = r'^[A-Za-z0-9_]+$'
    return bool(re.match(pattern, variable_name))


def is_flag(argument: str) -> bool:
    pattern = r"^-([a-zA-Z]+)$"
    return bool(re.match(pattern, argument))


def valid_exit_code(exit_code) -> bool:
    try:
        int(exit_code)
    except ValueError:
        return False
    else:
        return True


def invalid_option_pwd(options: list) -> str:
    for option in options:
        if option != "P":
            return option
    return ""
