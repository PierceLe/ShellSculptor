"""
exit_command.py

Defines the "Exit" command class, responsinle for terminating the shell
process with optional exit codes.

Classes:
    - Exit: Exits the shell with a given exit code.
"""

import sys
import validate
import parsing

from mysh_command import Command


class Exit(Command):
    """
    Exits the shell process.

    Provides functionality to terminate the shell with an optional exit code.
    If no code is given, the default is 0.

    """
    def execute(self):
        """
        Executes the `exit` command.

        Checks the arguments provided with the `exit` command:
        - No arguments are provided -> exit with code 0.
        - One argument is provided -> checks if the argument is a valid
          integer, exits with that code. If not an integer, prints an 
          error message.
        - More than one argument is provided -> prints an error message
          complaining that too many arguments were given.

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
