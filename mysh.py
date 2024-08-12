import signal
import shlex

from Cd import Cd
from Exit import Exit
from Pwd import Pwd
import os

# DO NOT REMOVE THIS FUNCTION!
# This function is required in order to correctly switch the terminal foreground group to
# that of a child process.
def setup_signals() -> None:
    """
    Setup signals required by this program.
    """
    signal.signal(signal.SIGTTOU, signal.SIG_IGN)

def split_arguments(command: str) -> list:
    try:
        command_argument = shlex.split(command)
        return command_argument
    except ValueError:
        return []


def main() -> None:
    # DO NOT REMOVE THIS FUNCTION CALL!
    setup_signals()
    while True:
        try:
            command = input(">> ")
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
            exit_command = Exit(command_argument)
            exit_command.execute()
        elif command_argument[0] == "pwd":
            pwd_command = Pwd(command_argument)
            pwd_command.execute()
        elif command_argument[0] == "cd":
            cd_command = Cd(command_argument)
            cd_command.execute()
        elif command_argument[0] == "mkdir":
            pass


if __name__ == "__main__":
    main()

