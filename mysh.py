import signal


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

    # Start your code here!


if __name__ == "__main__":
    main()
