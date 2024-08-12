import os
import sys
from Command import Command


def invalid_option(options: list) -> str:
    for option in options:
        if option != "P":
            return option
    return ""


class Pwd(Command):
    def execute(self):
        if len(self._argument) == 1:
            print(os.getcwd())
            pass
            # execute pwd Command
        elif len(self._argument) >= 2:
            if self._argument[1].startswith("-"):
                options: list = list(self._argument[1])[1:]
                if len(options) == 1 and options[0] == "P":
                    print(os.getcwd())
                    # execute command pwd -P
                else:
                    print(f"pwd: invalid option: -{invalid_option(options)}")
            else:
                print("pwd: not expecting any arguments", file=sys.stderr)
        elif len(self._argument) > 2:
            print(f"pwd: invalid option: {self._argument[2]}")
