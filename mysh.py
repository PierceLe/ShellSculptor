"""
mysh.py

Serves as the main entry point for the program. handles the setup of required
signals, loads config files, enter loop to accept and execute commands.

Functions:
    - setup_signals(): Sets up necessary signal handling.
    - main(): Runs the shell, handling input, parsing, execute commands, 
    and manage signals.
"""


import signal
import os
import sys

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
    """
    The main function that runs the shell program.

    Initializes the shell by setting up signals and loading config files. Enter a
    loop to repeatedly promts for input, parses the input and executes the command.

    Handles various exceptions such as EOF and keyboard interrupts to ensure 
    smooth operation.
    """
    setup_signals()
    # load_config_file()
    test_mode = "--runtest" in sys.argv

    # Set prompt behavior based on test mode
    show_prompt = not test_mode

    while True:
        try:
            load_config_file()
            prompt = os.environ.get("PROMPT")
            if show_prompt:
                command = input(f"{prompt}")
            else:
                command = input()
                print(f"{prompt}{command}", flush=True)
        except EOFError:
            print()
            break
        except KeyboardInterrupt:
            print()
            continue
        if command.strip() == "":
            continue
        command_argument: list = split_arguments(command)
        if not command_argument:
            print("mysh: syntax error: unterminated quote")
            continue
        command_type: Command = command_factory(command)
        command_type.execute()


if __name__ == "__main__":
    main()
