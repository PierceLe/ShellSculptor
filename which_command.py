"""
which_command.py

This module provides the implementation of the Which command,
which is used to locate a command's executable file in the system's PATH.
"""

import os
import sys
import parsing
from mysh_command import Command

BUILTIN_COMMANDS: list = ["cd", "pwd", "exit", "var", "which"]

"""
This module provides the implementation of the Which command, 
which is used to locate a command's executable file in the system's PATH.
"""


class Which(Command):
    """
    Which class provides methods to locate the executable path
    for a given command using the system's PATH.
    """
    def execute_file(self, command: str):
        """
        This module provides the implementation of the Which command,
        which is used to locate a command's executable file in the system's PATH.
        """
        if command in BUILTIN_COMMANDS:
            return f"{command}: shell built-in command"
        paths = os.getenv('PATH', os.defpath).split(os.pathsep)
        for path in paths:
            full_path = os.path.join(path, command)
            if os.path.isfile(full_path) and os.access(full_path, os.X_OK):
                return full_path
        return f"{command} not found"

    def execute(self):
        commands: list = parsing.split_arguments(self._command)[1:]
        if len(commands) == 0:
            print("usage: which command ...", file=sys.stderr)
        for command in commands:
            print(self.execute_file(command))
