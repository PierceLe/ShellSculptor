"""
pwd_command.py

This module provides the implementation of the Pwd command,
which prints the current working directory to the console.
It supports options like `-P` to display the physical directory without symbolic links.
"""

import os
import sys
from mysh_command import Command
import validate
import parsing


class Pwd(Command):
    """
    The Pwd class provides functionality to execute the `pwd` command in the shell.
    It supports printing the current working directory and handling options like `-P`.
    """
    def execute(self):
        """
        Executes the `pwd` command based on the provided arguments.

        If no arguments are provided, it prints the current directory stored in
        the PWD environment variable. If the `-P` option is provided, it prints
        the physical directory without symbolic links. It handles invalid options
        and unexpected arguments by printing appropriate error messages.
        """
        argument: list = parsing.split_arguments(self._command)
        if len(argument) == 1:
            print(os.environ['PWD'])
            # execute pwd Command
        elif len(argument) >= 2:
            if argument[1].startswith("-"):
                options: list = list(argument[1])[1:]
                if len(options) == 1 and options[0] == "P":
                    print(os.getcwd())
                    # execute command pwd -P
                else:
                    print(f"pwd: invalid option: -{validate.invalid_option_pwd(options)}")
            else:
                print("pwd: not expecting any arguments", file=sys.stderr)
        elif len(argument) > 2:
            print(f"pwd: invalid option: {argument[2]}")
