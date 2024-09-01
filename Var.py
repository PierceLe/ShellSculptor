import os
import sys
import re
from Command import Command
from Which import Which
import Verify
from ExecuteCommand import ExecuteCommand

class Var(Command):
    def shell_variable(self, command):
        pattern_detect_variable = r"\\?\$\{(.*?)\}"

        def replace_match(match):
            full_match = match.group(0)
            variable_name = match.group(1)

            if full_match.startswith('\\$'):
                return full_match[1:]

            if not Verify.valid_variable_name(variable_name):
                print(f"mysh: syntax error: invalid characters for variable '{variable_name}'", file=sys.stderr)
                return full_match
            return os.environ.get(variable_name, "")

        result = re.sub(pattern_detect_variable, replace_match, command)
        return result

    def is_flag(self, argument: str) -> bool:
        """Check if the argument is a valid flag."""
        return bool(re.match(r"^-([a-zA-Z]+)$", argument))

    def execute_command_and_capture_output(self, command: str) -> str:
        """Execute a command and return its output using ExecuteCommand."""
        execute_command = ExecuteCommand(command)
        rside, wside = os.pipe()

        if os.fork() == 0:
            os.close(rside)
            os.dup2(wside, 1)

            execute_command.execute()
            os._exit(0)

        os.close(wside)
        pyrside = os.fdopen(rside)
        output = pyrside.read()
        pyrside.close()
        os.waitpid(-1, 0)
        return output
    def execute(self):
        if len(self._argument) not in [3, 4]:
            print(f"var: expected 2 arguments, got {len(self._argument) - 1}")
            return

        if self.is_flag(self._argument[1]):
            if self._argument[1] != "-s":
                print(f"var: invalid option: {self._argument[1][: 2]}")
                return
            
            variable_name = self._argument[2]
            if not Verify.valid_variable_name(variable_name):
                print(f"var: invalid characters for variable {self._argument[2]}", file=sys.stderr)
                return
            command_to_execute = self._argument[3]
            output = self.execute_command_and_capture_output(command_to_execute)
            os.environ[variable_name] = output

        elif Verify.valid_variable_name(self._argument[1]):
            if len(self._argument) == 3:
                os.environ[self._argument[1]] = self.shell_variable(self._argument[2])
            else:
                print(f"var: expected 2 arguments, got {len(self._argument) - 1}")
        else:
            print(f"var: invalid characters for variable {self._argument[1]}", file=sys.stderr)
