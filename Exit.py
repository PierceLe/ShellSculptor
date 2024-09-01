from Command import Command
import Verify
import sys


class Exit(Command):

    def execute(self):
        if len(self._argument) == 1:
            exit(0)
        elif len(self._argument) == 2:
            exit_code = self._argument[1]
            if Verify.valid_exit_code(exit_code):
                exit(int(exit_code))
            else:
                print(f"exit: non-integer exit code provided: {self._argument[1]}", file=sys.stderr)
        elif len(self._argument) > 2:
            print("exit: too many arguments", file=sys.stderr)
