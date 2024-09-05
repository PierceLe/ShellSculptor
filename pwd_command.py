"""
pwd_command.py

Provides the implementation of the Pwd command,printing the 
current working directory to the console. Supports options like 
`-P` to display the physical directory without symbolic links.
"""

import os
import sys
from mysh_command import Command
import validate
import parsing


class Pwd(Command):
    """
    Provides functionality to execute the `pwd` command in the shell.
    Supports printing the current working directory and handling options like `-P`.
    """
    def execute(self):
        """
        Executes the `pwd` command based on the provided arguments.

        No arguments -> prints the current directory stored in the 
        PWD environment variable. 
        
        `-P` option is provided -> prints the physical directory without 
        symbolic links. Handles invalid options and unexpected arguments 
        via printing appropriate error messages.
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
                    print(
                        f"pwd: invalid option: -{validate.invalid_option_pwd(options)}",
                        file=sys.stderr
                    )
            else:
                print("pwd: not expecting any arguments", file=sys.stderr)
        elif len(argument) > 2:
            print(f"pwd: invalid option: {argument[2]}", file=sys.stderr)
