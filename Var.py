import os
import sys
from Command import Command
import Verify
from ExecuteCommand import ExecuteCommand
from parsing import solving_shell_variable


def execute_command_and_capture_output(command: str) -> str:
    """Execute a command and return its output using ExecuteCommand."""
    execute_command = ExecuteCommand(command)
    rside, wside = os.pipe()

    if os.fork() == 0:
        os.close(rside)
        os.dup2(wside, 1)
        execute_command.execute()
        exit(0)

    os.close(wside)
    pyrside = os.fdopen(rside)
    output = pyrside.read()
    pyrside.close()
    os.waitpid(-1, 0)
    return output


class Var(Command):

    def execute(self):
        if len(self._argument) not in [3, 4]:
            print(f"var: expected 2 arguments, got {len(self._argument) - 1}")
            return

        if Verify.is_flag(self._argument[1]):
            if self._argument[1] != "-s":
                print(f"var: invalid option: {self._argument[1][: 2]}")
                return

            variable_name = solving_shell_variable(self._argument[2])
            if not variable_name:
                return
            if not Verify.valid_variable_name(variable_name):
                print(f"var: invalid characters for variable {self._argument[2]}", file=sys.stderr)
                return
            command_to_execute = self._argument[3]
            output = execute_command_and_capture_output(command_to_execute)
            os.environ[variable_name] = solving_shell_variable(output)

        elif Verify.valid_variable_name(self._argument[1]):
            if len(self._argument) == 3:
                os.environ[self._argument[1]] = solving_shell_variable((self._argument[2]))
            else:
                print(f"var: expected 2 arguments, got {len(self._argument) - 1}")
        else:
            print(f"var: invalid characters for variable {self._argument[1]}", file=sys.stderr)
