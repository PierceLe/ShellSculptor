import sys
import re
import os
import Verify
import shlex
from Which import Which
from parsing import split_by_pipe_op


class ExecuteCommand:
    def __init__(self, command: str):
        self.command = command
    
    def execute_pipeline(self, commands):
        num_commands = len(commands)
        pipes = []

        for i in range(num_commands - 1):
            pipes.append(os.pipe())

        for i, command in enumerate(commands):
            if i == 0:
                r, w = None, pipes[i][1]
            elif i == num_commands - 1:
                r, w = pipes[i - 1][0], None
            else:
                r, w = pipes[i - 1][0], pipes[i][1]

            pid = os.fork()

            if pid == 0:
                if r is not None:
                    os.dup2(r, 0)  # Redirect stdin
                    os.close(r)
                if w is not None:
                    os.dup2(w, 1)  # Redirect stdout
                    os.close(w)

                for pr, pw in pipes:
                    os.close(pr)
                    os.close(pw)

                command_args = self.split_arguments(command)
                try:
                    os.execvp(command_args[0], command_args)
                except FileNotFoundError:
                    print(f"mysh: command not found: {command_args[0]}", file=sys.stderr)
                    sys.exit(1)

            else:
                if r is not None:
                    os.close(r)
                if w is not None:
                    os.close(w)

        for _ in range(num_commands):
            os.wait()

    def split_arguments(self, command: str) -> list:
        try:
            s = shlex.shlex(command, posix=True)
            s.escapedquotes = "'\""
            s.whitespace_split = True
            return [os.path.expanduser(arg) for arg in list(s)]
        except ValueError:
            return []

    def shell_variable(self, command):
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

    def execute(self):
        if '|' in self.command:
            commands = split_by_pipe_op(self.command)
            for command in commands:
                if not command.strip():
                    print("mysh: syntax error: expected command after pipe", file=sys.stderr)
                    return None
        else:
            commands = [self.command]
        
        final_command = []
        for command in commands:
            final_command.append(self.shell_variable(command))
        
        prev_fd = None  # To store the file descriptor of the previous command
        for i, command in enumerate(final_command):
            command_argument = self.split_arguments(command)

            if i == len(final_command) - 1:
                # Last command, no need for piping
                rside, wside = None, None
            else:
                # For all commands except the last one, create a pipe
                rside, wside = os.pipe()

            pid = os.fork()
            if pid == 0:  # Child process
                if prev_fd:
                    os.dup2(prev_fd, 0)  # Set stdin to read from the previous command's output
                    os.close(prev_fd)

                if wside is not None:
                    os.dup2(wside, 1)  # Set stdout to write to the pipe
                    os.close(wside)

                # Close any remaining pipe descriptors in the child process
                if rside is not None:
                    os.close(rside)

                executable_command = command_argument[0]

                if os.path.isfile(executable_command):
                    if not os.access(executable_command, os.X_OK):
                        print(f"mysh: permission denied: {executable_command}", file=sys.stderr)
                        os._exit(1)
                    # If the command is a file and is executable, set executable_path to the command itself
                    executable_path = executable_command
                else:
                    which_command = Which(["which", executable_command])
                    executable_path = which_command.execute_file(executable_command)
                    if executable_path == f"{executable_command} not found":
                        print(f"mysh: command not found: {executable_command}", file=sys.stderr)
                        os._exit(1)
                    if not executable_path:
                        print(f"mysh: no such file or directory: {command_argument[0]}", file=sys.stderr)
                        os._exit(1)

                os.execve(executable_path, command_argument, os.environ)

            else:  # Parent process
                if prev_fd:
                    os.close(prev_fd)  # Close the previous file descriptor
                if wside:
                    os.close(wside)  # Close the write side of the pipe in the parent
                prev_fd = rside  # Set up for the next iteration

        # Wait for all child processes to finish
        for _ in range(len(final_command)):
            os.wait()

        # Clean up the last pipe's read side if it was opened
        if prev_fd is not None:
            os.close(prev_fd)
