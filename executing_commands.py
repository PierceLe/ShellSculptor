"""
execute_command.py

This module defines the `ExecuteCommand` class, which is responsible for
executing shell commands in the shell environment. It handles both
single commands and piped commands, managing process creation and
execution while handling errors and permissions.

Classes:
    - ExecuteCommand: A command class that executes shell commands, with support
      for piping and variable substitution.
"""

import sys
import os
from which_command import Which
from mysh_command import Command
from parsing import split_by_pipe_op, solving_shell_variable, split_arguments


class ExecuteCommand(Command):
    """
    A command class that executes shell commands.

    The `ExecuteCommand` class is designed to handle the execution of shell
    commands. It supports commands with pipes, handles shell variable
    substitution, and manages process creation and execution, ensuring that
    errors and permissions are properly managed.
    """

    def execute(self):
        """
        Executes the shell command.

        This method processes the command string, handling shell variable
        substitution, command splitting (for pipes), and the execution of
        individual commands. If the command contains pipes, it sets up the
        necessary pipes and forks child processes to execute each command
        in the pipeline. It also manages permissions, checking if a command
        is executable and handling any errors that occur.

        Raises:
            SystemExit: Exits the shell if a command is not found or cannot be executed.
        """
        if not solving_shell_variable(self._command):
            return

        commands = self._prepare_commands()
        if not commands:  # Check for an empty list
            return

        self._execute_commands(commands)

    def _prepare_commands(self):
        """Prepare the commands for execution by splitting pipes and handling errors."""
        if '|' in self._command:
            commands = split_by_pipe_op(self._command)
            if any(not command.strip() for command in commands):
                print("mysh: syntax error: expected command after pipe", file=sys.stderr)
                return []
        else:
            commands = [self._command]

        return [solving_shell_variable(command) for command in commands]

    def _execute_commands(self, commands):
        """Execute the list of commands, handling pipes and process management."""
        prev_fd = None

        for i, command in enumerate(commands):
            command_argument = split_arguments(command)
            rside, wside = self._setup_pipes(i, len(commands))

            pid = os.fork()
            if pid == 0:  # Child process
                self._setup_child_process(prev_fd, wside)
                self._execute_command(command_argument)
            else:  # Parent process
                prev_fd = self._handle_parent_process(pid, prev_fd, rside, wside)

        if prev_fd is not None:
            os.close(prev_fd)

    def _setup_pipes(self, index, total_commands):
        """Setup pipes for command execution based on its position in the pipeline."""
        if index == total_commands - 1:
            return None, None
        return os.pipe()

    def _setup_child_process(self, prev_fd, wside):
        """
        Setup the child process, redirecting input/output
        and closing unnecessary file descriptors.
        """
        os.setpgid(0, 0)
        if prev_fd:
            os.dup2(prev_fd, 0)
            os.close(prev_fd)
        if wside is not None:
            os.dup2(wside, 1)
            os.close(wside)

    def _execute_command(self, command_argument):
        """Execute the actual command, handling file existence and permissions."""
        executable_command = command_argument[0]

        if os.path.isfile(executable_command):
            if not os.access(executable_command, os.X_OK):
                print(f"mysh: permission denied: {executable_command}", file=sys.stderr)
                sys.exit()
            executable_path = executable_command
        else:
            executable_path = self._find_executable_path(executable_command)

        os.execve(executable_path, command_argument, os.environ)

    def _find_executable_path(self, executable_command):
        """Find the executable path using the 'which' command or exit if not found."""
        which_command = Which(f"which {executable_command}")
        executable_path = which_command.execute_file(executable_command)
        if executable_path == f"{executable_command} not found":
            print(f"mysh: command not found: {executable_command}", file=sys.stderr)
            sys.exit()
        if not executable_path:
            print(f"mysh: no such file or directory: {executable_command}", file=sys.stderr)
            sys.exit()
        return executable_path

    def _handle_parent_process(self, pid, prev_fd, rside, wside):
        """
        Handle the parent process responsibilities, including closing pipes
        and waiting for the child.
        """
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

        return rside
