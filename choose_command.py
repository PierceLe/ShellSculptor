import parsing
from mysh_command import Command
from cd_command import Cd
from exit_command import Exit
from pwd_command import Pwd
from which_command import Which
from var_command import Var
from executing_commands import ExecuteCommand


def command_factory(command: str) -> Command:
    command_argument: list = parsing.split_arguments(command)
    if command_argument[0] == "exit":
        return Exit(command)
    if command_argument[0] == "pwd":
        return Pwd(command)
    if command_argument[0] == "cd":
        return Cd(command)
    if command_argument[0] == "var":
        return Var(command)
    if command_argument[0] == "which":
        return Which(command)
    return ExecuteCommand(command)
