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

        This method changes the current working directory based on the
        provided path. If no path is provided, it defaults to the user's
        home directory. It updates the `PWD` environment variable to reflect
        the new working directory.

        Handles the following cases:
        - No arguments: Changes to the home directory.
        - Too many arguments: Prints an error message.
        - Path resolution: Expands user directories, handles absolute and
        relative paths.
        - Updates the `PWD` environment variable accordingly.

        Error Handling:
        - PermissionError: Prints an error if the user does not have
        permission to change to the specified directory.
        - FileNotFoundError: Prints an error if the specified directory
        does not exist.
        - NotADirectoryError: Prints an error if the specified path is
        not a directory.
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
