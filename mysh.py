import signal
import shlex


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
    except (ValueError):
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
        if command.strip() == "exit":
            print("exit")
            break
        print(command)
        command_argument: list = split_arguments(command)
        if command_argument == []:
            print("mysh: syntax error: unterminated quote")
        else:
            print(command_argument)
            
    

if __name__ == "__main__":
    main()
