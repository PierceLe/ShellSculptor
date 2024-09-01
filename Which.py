import os
import sys
import parsing
from Command import Command

BUILTIN_COMMANDS: list = ["cd", "pwd", "exit", "var", "which"]


class Which(Command):

    def execute_file(self, command: str):
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
            print(f"usage: which command ...", file=sys.stderr)
        for command in commands:
            print(self.execute_file(command))

