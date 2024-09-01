import os
import sys
from Command import Command
import Verify


class Pwd(Command):
    def execute(self):
        if len(self._argument) == 1:
            print(os.environ['PWD'])
            # execute pwd Command
        elif len(self._argument) >= 2:
            if self._argument[1].startswith("-"):
                options: list = list(self._argument[1])[1:]
                if len(options) == 1 and options[0] == "P":
                    print(os.getcwd())
                    # execute command pwd -P
                else:
                    print(f"pwd: invalid option: -{Verify.invalid_option_pwd(options)}")
            else:
                print("pwd: not expecting any arguments", file=sys.stderr)
        elif len(self._argument) > 2:
            print(f"pwd: invalid option: {self._argument[2]}")
