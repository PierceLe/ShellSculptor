import signal
import shlex

from Cd import Cd
from Exit import Exit
from Pwd import Pwd
from Which import Which

# DO NOT REMOVE THIS FUNCTION!
# This function is required in order to correctly switch the terminal foreground group to
# that of a child process.

BUILTIN_COMMANDS: list = ["cd", "pwd", "exit", "cd", "var"]


def setup_signals() -> None:
    """
    Setup signals required by this program.
    """
    signal.signal(signal.SIGTTOU, signal.SIG_IGN)


def split_arguments(command: str) -> list:
    try:
        s = shlex.shlex(command, posix=True)
        s.escapedquotes = "'\""
        s.whitespace_split = True
        return list(s)
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
        # elif command_argument[0] == "var":
        #     var_command = Variable(command_argument)
        #     var_command.execute()
        elif command_argument[0] == "which":
            which_command = Which(BUILTIN_COMMANDS, command_argument)
            which_command.execute()


if __name__ == "__main__":
    main()
