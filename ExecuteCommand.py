import sys
import os
from Which import Which
from Command import Command
from parsing import split_by_pipe_op
from parsing import solving_shell_variable
from parsing import split_arguments


class ExecuteCommand(Command):
    def __init__(self, command: str, argument: list):
        super().__init__(argument)
        self.command = command

    def execute(self):
        if not solving_shell_variable(self.command):
            return
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
            final_command.append(solving_shell_variable(command))

        prev_fd = None  # To store the file descriptor of the previous command
        for i, command in enumerate(final_command):
            command_argument = split_arguments(command)

            if i == len(final_command) - 1:
                # Last command, no need for piping
                rside, wside = None, None
            else:
                # For all commands except the last one, create a pipe
                rside, wside = os.pipe()

            pid = os.fork()
            if pid == 0:  # Child process
                os.setpgid(0, 0)
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
                        exit()
                    # If the command is a file and is executable, set executable_path to the command itself
                    executable_path = executable_command
                else:
                    which_command = Which(["which", executable_command])
                    executable_path = which_command.execute_file(executable_command)
                    if executable_path == f"{executable_command} not found":
                        print(f"mysh: command not found: {executable_command}", file=sys.stderr)
                        exit()
                    if not executable_path:
                        print(f"mysh: no such file or directory: {command_argument[0]}", file=sys.stderr)
                        exit()

                os.execve(executable_path, command_argument, os.environ)

            else:  # Parent process
                try:
                    os.setpgid(pid, pid)
                except PermissionError:
                    pass
                fd = os.open("/dev/tty", os.O_RDWR)
                os.tcsetpgrp(fd, os.getpgid(pid))
                os.wait()
                os.tcsetpgrp(fd, os.getpgid(0))
                if prev_fd:
                    os.close(prev_fd)
                if wside:
                    os.close(wside)
                prev_fd = rside

        if prev_fd is not None:
            os.close(prev_fd)
