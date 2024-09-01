from abc import ABC, abstractmethod


class Command(ABC):
    def __init__(self, command: str):
        self._command = command

    @property
    def get_command(self) -> str:
        return self._command

    @abstractmethod
    def execute(self) -> None:
        pass
