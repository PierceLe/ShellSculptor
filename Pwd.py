import os
import sys
from Command import Command
import Verify
import parsing


class Pwd(Command):
    def execute(self):
        argument: list = parsing.split_arguments(self._command)
        if len(argument) == 1:
            print(os.environ['PWD'])
            # execute pwd Command
        elif len(argument) >= 2:
            if argument[1].startswith("-"):
                options: list = list(argument[1])[1:]
                if len(options) == 1 and options[0] == "P":
                    print(os.getcwd())
                    # execute command pwd -P
                else:
                    print(f"pwd: invalid option: -{Verify.invalid_option_pwd(options)}")
            else:
                print("pwd: not expecting any arguments", file=sys.stderr)
        elif len(argument) > 2:
            print(f"pwd: invalid option: {argument[2]}")
