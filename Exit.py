from Command import Command
import sys

class Exit(Command):
    def valid_code(self, exit_code) -> bool:
        try: 
            int(exit_code)
        except ValueError:
            return False
        else:
            return True

    
    def execute(self):
        if len(self._argument) == 1:
            exit(0)
        elif len(self._argument) == 2:
            exit_code = self._argument[1]
            if (self.valid_code(exit_code)):
                exit(exit_code)
            else:
                print(f"exit: non-integer exit code provided: {self._argument[1]}", file=sys.stderr)
        elif len(self._argument > 2):
            print("exit: too many arguments", file=sys.stderr)