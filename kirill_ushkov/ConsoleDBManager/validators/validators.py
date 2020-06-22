from abc import ABC, abstractmethod
from .errors import InputError


class Validator(ABC):

    @abstractmethod
    def validate(self, string):
        pass


class CommandValidator(Validator):
    def __init__(self, command_type):
        self.command_type = command_type

    def validate(self, string):
        commands = string.split()
        if len(commands) < 2 or len(commands) > 2:
            raise InputError("Too many arguments","Command expects 2 arguments")

        if commands[0] == self.command_type.value:
            return commands[0]
        else:
            raise InputError("Unrecognized command", "")
