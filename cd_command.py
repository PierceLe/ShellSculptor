"""
cd_command.py

This module defines the `Cd` class which handles changing directories.

Classes:
    - Cd: changes the current directory of the shell.
"""

import sys
import os
import parsing
from mysh_command import Command


class Cd(Command):
    """
    Handles the 'cd' command, allowing for changing the current working directory.
    Supports going to home directory, relative paths and absolute paths. Also
    handles errors like permission denied, non-existent directories and changing
    to a non-directory file.
    """
    def execute(self):
        """
        Executes the `cd` command.

        Changes current working directory to the provided path, if none
        is provided then it defaults to user's home directory. Updates the
        "PWD" enviroment variable to show the new working directory.

        Cases:
        - No arguments: to home directory
        - Too many arguments: error message
        - Path resolution: expand user directories, both absolute and
        relative paths
        - Updates the "PWD" variable accordingly


        Errors:
        - PermissionError: Prints an error if no permission to access
        directory.
        - FileNotFoundError: Prints an error if non-existent directory.
        - NotADirectoryError: Prints an error if path is not a directory.

        Raises:
            PermissionError: If no permission to access.
            FileNotFoundError: If non-existent directory.
            NotADirectoryError: If path is not a directory.
        """
        argument: list = parsing.split_arguments(self._command)
        if len(argument) == 1:
            path = os.path.expanduser("~")
        elif len(argument) > 2:
            print("cd: too many arguments", file=sys.stderr)
            return
        else:
            path = os.path.expanduser(argument[1])
        try:
            resolved_path = os.path.abspath(path)
            os.chdir(resolved_path)
            os.environ['PWD'] = resolved_path
        except PermissionError:
            print(f"cd: permission denied: {path}", file=sys.stderr)
        except FileNotFoundError:
            print(f"cd: no such file or directory: {path}", file=sys.stderr)
        except NotADirectoryError:
            print(f"cd: not a directory: {path}", file=sys.stderr)
