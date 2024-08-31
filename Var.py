import os
import sys
import re
from Command import Command


class Var(Command):

    def isFlag(self, argument: str) -> bool:
        pattern = r"^-([a-zA-Z]+)$"
        return bool(re.match(pattern, argument))

    def execute(self):
        if len(self._argument) == 1 or len(self._argument) == 2:
            # this means that the command line will be var. return Error
            print(f"var: expected 2 arguments, got {len(self._argument) - 1}")
        elif self.isFlag(self._argument[1]):
            # the situation that var have flags. IDK how to do this one
            pass
        elif self.valid_variable_name(self._argument[1]):
            # the situation that var did not have flags and valid name
            if len(self._argument) == 3:
                os.environ[f"{self._argument[1]}"] = self._argument[2]
            else:
                print(f"var: expected 2 arguments, got {len(self._argument) - 1}")
