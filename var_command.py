"""
var_command.py

Provides the implementation of the Var command, which is for setting and 
managing environment variables in the shell.
"""

import os
import sys
from mysh_command import Command
import validate
from executing_commands import ExecuteCommand
import parsing


def execute_command_and_capture_output(command: str) -> str:
    """Execute a command and return its output via ExecuteCommand."""
    execute_command = ExecuteCommand(command)
    rside, wside = os.pipe()

    if os.fork() == 0:
        os.close(rside)
        os.dup2(wside, 1)
        execute_command.execute()
        sys.exit(0)

    os.close(wside)
    pyrside = os.fdopen(rside)
    output = pyrside.read()
    pyrside.close()
    os.waitpid(-1, 0)
    return output


class Var(Command):
    """
    Provides functionality to set and manage environment variables. Supports 
    both simple assignment of variables and executing commands to set variables to
    the outputs.
    """
    def execute(self):
        argument: list = parsing.split_arguments(self._command)
        if len(argument) not in [3, 4]:
            print(f"var: expected 2 arguments, got {len(argument) - 1}")
            return

        if validate.is_flag(argument[1]):
            for flag in argument[1][1:]:
                if flag != 's':
                    print(f"var: invalid option: -{flag}")
                    break
            if len(argument) < 4:
                print(f"var: expected 4 arguments, got {len(argument) - 1}", file=sys.stderr)
                return
            variable_name = parsing.solving_shell_variable(argument[2])
            if not variable_name:
                return
            if not validate.valid_variable_name(variable_name):
                print(f"var: invalid characters for variable {argument[2]}", file=sys.stderr)
                return
            command_to_execute = argument[3]
            output = execute_command_and_capture_output(command_to_execute)
            os.environ[variable_name] = parsing.solving_shell_variable(output)

        elif validate.valid_variable_name(argument[1]):
            if len(argument) == 3:
                os.environ[argument[1]] = parsing.solving_shell_variable((argument[2]))
            else:
                print(f"var: expected 2 arguments, got {len(argument) - 1}")
        else:
            print(f"var: invalid characters for variable {argument[1]}", file=sys.stderr)
