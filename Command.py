from abc import ABC, abstractmethod
from distutils.cmd import Command


class Command(ABC):
    def __init__(self, argument: list):
        self._argument = argument

    @property
    def argument(self) -> list:
        return self._argument

    @abstractmethod
    def execute(self):
        pass
