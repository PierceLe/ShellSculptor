"""
exit_command.py

This module defines the `Exit` command class, which is responsible for
terminating the shell process with an optional exit code.

Classes:
    - Exit: A command class that exits the shell with a given exit code.
"""


import sys
import validate
import parsing

from mysh_command import Command


class Exit(Command):
    """
    A command class that exits the shell process.

    The `Exit` class provides functionality to terminate the shell with an
    optional exit code. If no exit code is provided, the default exit code is 0.
    """
    def execute(self):
        """
        Executes the `exit` command.

        This method checks the arguments provided with the `exit` command:
        - If no arguments are provided, it exits the shell with code 0.
        - If one argument is provided, it checks if the argument is a valid
          integer and exits with that code. If the argument is not an integer,
          it prints an error message.
        - If more than one argument is provided, it prints an error message
          indicating that too many arguments were given.

        Raises:
            SystemExit: When the command is executed with a valid exit code.
        """
        argument: list = parsing.split_arguments(self._command)
        if len(argument) == 1:
            sys.exit(0)
        elif len(argument) == 2:
            exit_code = argument[1]
            if validate.valid_exit_code(exit_code):
                sys.exit(int(exit_code))
            else:
                print(f"exit: non-integer exit code provided: {argument[1]}", file=sys.stderr)
        elif len(argument) > 2:
            print("exit: too many arguments", file=sys.stderr)
