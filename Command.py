from abc import ABC, abstractmethod
import re


class Command(ABC):
    def __init__(self, argument: list):
        self._argument = argument

    def valid_variable_name(self, variable_name: str) -> bool:
        pattern = r'^[A-Za-z0-9_]+$'
        return bool(re.match(pattern, variable_name))

    @property
    def argument(self) -> list:
        return self._argument

    @abstractmethod
    def execute(self) -> None:
        pass
