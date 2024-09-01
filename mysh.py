import signal
import shlex
import os
import json
import sys
import re

from Cd import Cd
from Exit import Exit
from Pwd import Pwd
from Which import Which
from Var import Var
import Verify
from ExecuteCommand import ExecuteCommand

# DO NOT REMOVE THIS FUNCTION!
# This function is required in order to correctly switch the terminal foreground group to
# that of a child process.

BUILTIN_COMMANDS: list = ["cd", "pwd", "exit", "cd", "var", "which"]


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
def shell_variable(command):
    pattern_detect_variable = r"\\?\$\{(.*?)\}"

    def replace_match(match):
        full_match = match.group(0)
        variable_name = match.group(1)

        if full_match.startswith('\\$'):
            return full_match[1:]

        if not Verify.valid_variable_name(variable_name):
            print(f"mysh: syntax error: invalid characters for variable '{variable_name}'", file=sys.stderr)
            return full_match
        return os.environ.get(variable_name, "")

    result = re.sub(pattern_detect_variable, replace_match, command)
    return result


def load_config_file():
    myshdotdir = os.environ.get("MYSHDOTDIR")
    if myshdotdir:
        myshrc_path = os.path.join(myshdotdir, ".myshrc")
    else:
        home_dir = os.path.expanduser("~")
        myshrc_path = os.path.join(home_dir, ".myshrc")
    if not os.path.exists(myshrc_path):
        # case we cant find the file, continuing like default
        return
    
    try:
        with open(myshrc_path, "r") as file:
            env_variables = json.load(file)
    except json.JSONDecodeError:
        print("mysh: invalid JSON format for .myshrc", file=sys.stderr)
        return

    for key, value in env_variables.items():
        if not isinstance(value, str):
            print(f"mysh: .myshrc: {key}: not a string", file=sys.stderr)
            continue
        elif not Verify.valid_variable_name(key):
            print(f"mysh: .myshrc: {key}: invalid characters for variable name", file=sys.stderr)
            continue
        # print(key, value)
        os.environ[key] = shell_variable(os.path.expandvars(value))


    

def main() -> None:
    # DO NOT REMOVE THIS FUNCTION CALL!
    setup_signals()
    os.environ["PROMPT"] = ">> "
    os.environ["MYSH_VERSION"] = "1.0"
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
            exit_command = Exit(command_argument)
            exit_command.execute()
        elif command_argument[0] == "pwd":
            pwd_command = Pwd(command_argument)
            pwd_command.execute()
        elif command_argument[0] == "cd":
            cd_command = Cd(command_argument)
            cd_command.execute()
        elif command_argument[0] == "var":
            var_command = Var(command_argument)
            var_command.execute()
        elif command_argument[0] == "which":
            which_command = Which(command_argument)
            which_command.execute()
        else:
            execute_command = ExecuteCommand(command)
            execute_command.execute()


if __name__ == "__main__":
    main()

