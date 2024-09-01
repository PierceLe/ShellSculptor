import signal
import os

from mysh_command import Command
from configure_mysh import load_config_file
from parsing import split_arguments
from choose_command import command_factory


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

        command_type: Command = command_factory(command)
        command_type.execute()


if __name__ == "__main__":
    main()
