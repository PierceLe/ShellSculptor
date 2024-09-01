import os
import json
import sys
import Verify
from parsing import solving_shell_variable


def load_config_file():
    os.environ["PROMPT"] = os.environ.get("PROMPT", ">> ")
    os.environ["MYSH_VERSION"] = os.environ.get("MYSH_VERSION", "1.0")
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
        os.environ[key] = solving_shell_variable(value)
