"""
configure_mysh.py

This module provides functionality to load and apply shell configuration
settings from a `.myshrc` file. It sets up environment variables for the shell
based on the content of the configuration file or defaults if the file does not exist.

Functions:
    - load_config_file(): Loads configuration settings from the `.myshrc` file
      and sets environment variables accordingly.
"""

import os
import json
import sys
import validate
import parsing


def load_config_file():
    """
    Loads and applies settings from the `.myshrc` file.

    Checks for `.myshrc` file in the `MYSHDOTDIR` directory or in the home directory.
    If the file is found, the function reads the JSON-formatted enviroment variables
    from the file and sets them. If the file is not found or an error occurs 
    (example: invalid JSON) then the function prints an error message and continues
    with default.

    Environment variables set:
    - PROMPT: The shell prompt string.
    - MYSH_VERSION: The shell's version.

    Errors handled:
    - Missing `.myshrc` file: Continues with default settings.
    - Invalid JSON format: An error message is printed, continues with default settings.
    - Non-string values or invalid variable names: Skipped with an error message.

    Notes:
    - The shell variables are processed for shell-specific syntax
      before being set as environment variables.
    """
    os.environ["PROMPT"] = os.environ.get("PROMPT", ">> ")
    os.environ["MYSH_VERSION"] = os.environ.get("MYSH_VERSION", "1.0")
    myshdotdir = os.environ.get("MYSHDOTDIR")
    if myshdotdir:
        myshrc_path = os.path.join(myshdotdir, ".myshrc")
    else:
        home_dir = os.path.expanduser("~")
        myshrc_path = os.path.join(home_dir, ".myshrc")

    if not os.path.exists(myshrc_path):
        # case we cant find the file, continuing like default
        return

    try:
        with open(myshrc_path, "r", encoding="utf-8") as file:
            env_variables = json.load(file)
    except json.JSONDecodeError:
        print("mysh: invalid JSON format for .myshrc", file=sys.stderr)
        return

    for key, value in env_variables.items():
        if not isinstance(value, str):
            print(f"mysh: .myshrc: {key}: not a string", file=sys.stderr)
            continue
        if not validate.valid_variable_name(key):
            print(f"mysh: .myshrc: {key}: invalid characters for variable name", file=sys.stderr)
            continue
        os.environ[key] = parsing.solving_shell_variable(value)
