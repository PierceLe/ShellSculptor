# ShellSculptor - Customizing a Unix-like Shell using Python

## How Does the Shell Translate a Line of Input into a Command?

When a user inputs a command, the shell processes it through the following steps:

1. **Input Handling**:
   - First, the shell checks whether the user intends to terminate the shell using `Ctrl+D`. If not, the shell continues.
   - If the input is an empty string, the shell displays a new prompt without taking further action.

2. **Tokenizing the Input**:
   - The `split_argument` function (from the `parsing` module) is used to split the command string into a list of arguments, handling quotes and whitespace.
   - If there are unterminated quotes, the shell prompts the user for further input until the quotes are closed.

3. **Command Identification**:
   - The shell uses the `command_factory` function (from the `choose_command` module) to determine the type of command based on the first word of the input. This follows the **Factory Method Pattern**.

4. **Command Execution**:
   - Commands are executed by specific subclasses of an abstract `Command` class (from the `mysh_command` module), such as `Exit`, `Pwd`, `Cd`, `Var`, `Which`, and `ExecuteCommand` (from the `exit_command`, `pwd_command`, `cd_command`, `var_command`, `which_command`, and `executing_command` modules, respectively).
   - If the command is built-in, the shell uses the corresponding subclass to execute it.
   - If it is an external command, the `ExecuteCommand` class handles execution, checking if the command exists and returning appropriate errors if it does not.

### Summary of Steps:
1. **Tokenize Input**: Input is split into tokens, handling spaces, quotes, and special characters.
2. **Command Matching**: The first token is identified as the command, while the remaining tokens are treated as arguments.
3. **Command Execution**: The appropriate `Command` subclass is instantiated and its `execute` method is called.

For example, in `cd_command.py`, the input is parsed to identify the directory argument, and the shell changes the current working directory accordingly.

---

## How Does the Shell Handle Environment Variables?

The shell handles environment variables using the `solving_shell_variable` function. Here is the step-by-step process:

1. **Identifying Variables**:
   - The shell uses a regular expression `\?\$\{(.*?)\}` to detect environment variables in the form `${VARIABLE_NAME}`.
   - This regex identifies variables with or without escaping (`\$` for escaped variables).

2. **Variable Substitution**:
   - If a variable is found and is not escaped, it is replaced with its value from the environment using the `_substitute_variable` helper function.
   - For example, `${HOME}` would be replaced by `/home/user`.

3. **Error Handling**:
   - If a variable name contains invalid characters, an error is flagged, and the function returns `False`, indicating a syntax error.

---

## How Does the Shell Handle Pipelines?

The `ExecuteCommand` class manages the execution of commands, including those involving pipelines (`|`). Here is how it works:

### 1. **Splitting Commands**:
- The `_prepare_commands` method splits the input string by the pipe (`|`) operator using `split_by_pipe_op`. Each part is treated as an individual command in the pipeline.

### 2. **Creating Pipes**:
- When a pipe is detected, the shell uses `os.pipe()` to create two file descriptors:
   - **Writing End (stdout)**: For the output of the first command.
   - **Reading End (stdin)**: For the input of the next command.

### 3. **Forking Processes**:
- The shell forks a new process for each command. The first output of command is connected to the writing end of the pipe, and the next command reads from the pipes reading end.

### 4. **Managing Processes**:
- The parent process manages the pipes, ensuring each child process communicates properly.
- The `_handle_parent_process` method waits for child processes and closes pipes when done.

### 5. **Executing Commands**:
- Each command is executed using the `_execute_command` method, which handles both built-in and external commands. If the command is part of a pipeline, its output is redirected to the next input of command via the pipe.


### 6. Methods Involved:

1. **_prepare_commands**:
   - Splits the command string by detecting pipes and prepares each command for execution.

2. **_execute_commands**:
   - Sets up the execution of each command, handling the pipes, forking child processes, and managing stdout and stdin redirection.

3. **_handle_parent_process**:
   - Manages the parent process, waits for child processes, and closes file descriptors when necessary.

4. **_execute_command**:
   - Executes individual commands and handles errors related to file permissions and command existence.


## Test Structure format

1. Test Directory
   All test files are stored under a specific directory (TEST_DIR_PATH=~/tests).
   - The test files follow a specific naming convention:
   - 	Input files: Use the .in extension.
   -	Expected output files: Use the .out extension.
   -	Actual output files: Generated during the test and use the .actual extension.
2. Test Execution
   - The test runner script (run_tests.sh) iterates over all subdirectories in the test directory, executing each test case one by one.
   -	For each test, the corresponding shell program (mysh.py) is run using the input file. The output of the shell is redirected to an .actual file.
   -	The script then compares the .actual output with the expected .out output using the diff command.
3. Test Result
   -	If the actual output matches the expected output, the test is marked as passed.
   -	If there is a difference, the script shows a detailed color-coded difference between the expected and actual outputs (green for correct lines, red for incorrect or missing lines).
   -	The results for each test are displayed, and a summary is provided at the end.
4. Test Data such as the csv files for testing, txt files for testing, folder, symbolics links for testing, .myshrc for testing is in `test_data` folder

5. Assumption: The test is only works on the Ed environment. The reason for that is the home directory on Ed is different from in yours computer such as ~ will be converted to /home otherwise, the other envrionment can be different 