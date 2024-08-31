import os
import sys
from Command import Command


class Which(Command):
    def __init__(self, build_in_commands: list, argument: list):
        super().__init__(argument)
        self.build_in_commands = build_in_commands
        
    def is_built_in_command(self, command: str):
        if command in self.build_in_commands:
            return True
        return False
    

    def execute_file(self, command: str):
        if self.is_built_in_command(command):
            return f"{command}: shell built-in command"
        paths = os.getenv('PATH', os.defpath).split(os.pathsep)
        for path in paths:
            full_path = os.path.join(path, command)
            if os.path.isfile(full_path) and os.access(full_path, os.X_OK):
                return full_path
        return f"{command}: command not found"

    def execute(self):
        commands: list = self._argument[1:]
        if len(commands) == 0:
            print(f"usage: which command ...", file=sys.stderr)
        for command in commands:
            print(self.execute_file(command))
