import Verify
import sys
import parsing

from Command import Command



class Exit(Command):

    def execute(self):
        argument: list = parsing.split_arguments(self._command)
        if len(argument) == 1:
            exit(0)
        elif len(argument) == 2:
            exit_code = argument[1]
            if Verify.valid_exit_code(exit_code):
                exit(int(exit_code))
            else:
                print(f"exit: non-integer exit code provided: {argument[1]}", file=sys.stderr)
        elif len(argument) > 2:
            print("exit: too many arguments", file=sys.stderr)
