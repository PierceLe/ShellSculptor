import os
import sys
from Command import Command
import Verify
from ExecuteCommand import ExecuteCommand
import parsing


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
        argument: list = parsing.split_arguments(self._command)
        if len(argument) not in [3, 4]:
            print(f"var: expected 2 arguments, got {len(argument) - 1}")
            return

        if Verify.is_flag(argument[1]):
            if argument[1] != "-s":
                print(f"var: invalid option: {argument[1][: 2]}")
                return

            variable_name = parsing.solving_shell_variable(argument[2])
            if not variable_name:
                return
            if not Verify.valid_variable_name(variable_name):
                print(f"var: invalid characters for variable {argument[2]}", file=sys.stderr)
                return
            command_to_execute = argument[3]
            output = execute_command_and_capture_output(command_to_execute)
            os.environ[variable_name] = parsing.solving_shell_variable(output)

        elif Verify.valid_variable_name(argument[1]):
            if len(argument) == 3:
                os.environ[argument[1]] = parsing.solving_shell_variable((argument[2]))
            else:
                print(f"var: expected 2 arguments, got {len(argument) - 1}")
        else:
            print(f"var: invalid characters for variable {argument[1]}", file=sys.stderr)
