import sys
import os
import parsing
from Command import Command


class Cd(Command):
    def execute(self):
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
