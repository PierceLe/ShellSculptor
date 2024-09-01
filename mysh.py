import signal
import os

from Cd import Cd
from Exit import Exit
from Pwd import Pwd
from Which import Which
from Var import Var
from ExecuteCommand import ExecuteCommand
from configure_mysh import load_config_file
from parsing import split_arguments


# DO NOT REMOVE THIS FUNCTION!
# This function is required in order to correctly switch the terminal foreground group to
# that of a child process.


def setup_signals() -> None:
    """
    Setup signals required by this program.
    """
    signal.signal(signal.SIGTTOU, signal.SIG_IGN)


def main() -> None:
    # DO NOT REMOVE THIS FUNCTION CALL!
    setup_signals()
    load_config_file()
    while True:
        try:
            prompt = os.environ.get("PROMPT")
            command = input(f"{prompt}")
        except EOFError:
            print()
            break
        except KeyboardInterrupt:
            print()
            continue
        if command == "":
            continue
        command_argument: list = split_arguments(command)
        if not command_argument:
            print("mysh: syntax error: unterminated quote")
        elif command_argument[0] == "exit":
            exit_command = Exit(command)
            exit_command.execute()
        elif command_argument[0] == "pwd":
            pwd_command = Pwd(command)
            pwd_command.execute()
        elif command_argument[0] == "cd":
            cd_command = Cd(command)
            cd_command.execute()
        elif command_argument[0] == "var":
            var_command = Var(command)
            var_command.execute()
        elif command_argument[0] == "which":
            which_command = Which(command)
            which_command.execute()
        else:
            execute_command = ExecuteCommand(command)
            execute_command.execute()


if __name__ == "__main__":
    main()
