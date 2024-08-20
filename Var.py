import os
import sys
import re
from Command import Command


class Var(Command):

    def execute_wihout_flags(self):
        pass

    def isFlag(self, argument: str) -> bool:
        pattern = r"^-([a-zA-Z]+)$"
        return bool(re.match(pattern, argument))

    def execute(self):
        if len(self._argument) == 1:
            # this means that the command line will be var. return Error
            print(f"var: expected 2 arguments, got {len(self._argument) - 1}")
        elif len(self._argument) == 2:
            print(f"var: expected 2 arguments, got {len(self._argument) - 1}")
        elif self.isFlag(self._argument[1]):
            # the situation that var have flags. IDK how to do this one
            pass
        elif self.valid_variable_name(self._argument[1]):
            # the situation that var did not have flags and valid name
            if len(self._argument) == 3:
                os.environ["{self._argument[2]}"] = self._argument[3]
            else:
                print(f"var: expected 2 arguments, got {len(self._argument) - 1}")
