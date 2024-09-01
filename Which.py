import os
import sys
from Command import Command

BUILTIN_COMMANDS: list = ["cd", "pwd", "exit", "cd", "var", "which"]

class Which(Command):
    def __init__(self, argument: list):
        super().__init__(argument)

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
        commands: list = self._argument[1:]
        if len(commands) == 0:
            print(f"usage: which command ...", file=sys.stderr)
        for command in commands:
            print(self.execute_file(command))

