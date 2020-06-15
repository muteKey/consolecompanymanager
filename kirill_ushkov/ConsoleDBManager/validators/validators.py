from abc import ABC, abstractmethod
from ..models.menu_item import Command
from .errors import CommandSyntaxError, CommandMismatchError, TooShortDepartmentNameError


class Validator(ABC):

    @abstractmethod
    def validate(self, string):
        pass


class AddNewDepartmentCommandValidator(Validator):

    def __init__(self):
        self.minimumDepNameLength = 2

    def validate(self, string):
        commands = string.split()

        if len(commands) < 2 or len(commands) > 2:
            raise CommandSyntaxError

        if commands[0] == Command.ADD_DEPARTMENT.value:
            dep_name = commands[1]
            if len(dep_name) < self.minimumDepNameLength:
                raise TooShortDepartmentNameError
            return dep_name
        else:
            raise CommandMismatchError


class SelectDepartmentCommandValidator(Validator):
    def validate(self, string):
        commands = string.split()

        if len(commands) < 2 or len(commands) > 2:
            raise CommandSyntaxError

        if commands[0] == Command.SELECT_DEPARTMENT.value:
            dep_name = commands[1]
            if len(dep_name) < 2:
                raise TooShortDepartmentNameError
            return dep_name
        else:
            raise CommandMismatchError
