"""
cd_command.py

This module defines the `Cd` class, which provides the functionality
for changing the current working directory in the shell environment.

Classes:
    - Cd: A command class that changes the current directory of the shell.
"""

import sys
import os
import parsing
from mysh_command import Command


class Cd(Command):
    """
    A command class that changes the current working directory.

    The `Cd` class handles the `cd` command, allowing the user to change
    the current working directory of the shell. It supports navigating to
    the home directory, relative paths, and absolute paths, while also
    handling various errors like permission issues, non-existent directories,
    and attempts to change to a non-directory file.
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

        Raises:
            PermissionError: If access to the directory is denied.
            FileNotFoundError: If the directory does not exist.
            NotADirectoryError: If the specified path is not a directory.
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
            os.chdir(path)
            if os.path.isabs(path):
                os.environ['PWD'] = path
            elif path == "..":
                os.environ['PWD'] = os.path.dirname(os.environ['PWD'])
            else:
                os.environ['PWD'] = os.path.join(os.environ['PWD'], path)
        except PermissionError:
            print(f"cd: permission denied: {path}", file=sys.stderr)
        except FileNotFoundError:
            print(f"cd: no such file or directory: {path}", file=sys.stderr)
        except NotADirectoryError:
            print(f"cd: not a directory: {path}", file=sys.stderr)
