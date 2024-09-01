from Command import Command
from Cd import Cd
from Exit import Exit
from Pwd import Pwd
from Which import Which
from Var import Var
from ExecuteCommand import ExecuteCommand


def choose_command(command_argument: list) -> Command:
    if command_argument[0] == "exit":
        return Exit(command_argument)
    elif command_argument[0] == "pwd":
        return Pwd(command_argument)
    elif command_argument[0] == "cd":
        return Cd(command_argument)
    elif command_argument[0] == "var":
        return Var(command_argument)
    elif command_argument[0] == "which":
        return Which(command_argument)
    else:
        return ExecuteCommand(command_argument)