from abc import ABC, abstractmethod


class Command(ABC):
    def __init__(self, argument: list):
        self._argument = argument

    @property
    def argument(self) -> list:
        return self._argument

    @abstractmethod
    def execute(self) -> None:
        pass
