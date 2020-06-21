from ..validators.errors import CommandSyntaxError
from abc import ABC, abstractmethod
import re


class Parser(ABC):
    @abstractmethod
    def parse(self):
        pass


class CommandParser(Parser):
    def __init__(self, user_input):
        self.user_input = user_input
        self.command = ""
        self.arguments = []

    def parse(self):
        commands = self.user_input.split()
        if len(commands) == 0:
            raise CommandSyntaxError
        self.command = commands[0]
        self.arguments = commands[1:]


class AddEmployeeCommandParser(Parser):
    def __init__(self, user_input):
        self.user_input = user_input
        self.number_of_arguments = 3
        self.first_name = ""
        self.last_name = ""
        self.position = ""

    def parse(self):
        components = self.user_input.split()
        components.pop(0)
        if len(components) == 0 or len(components) > self.number_of_arguments:
            raise CommandSyntaxError

        first_name_pattern = re.compile("[A-Za-z]{2,25}")
        is_correct_first_name = bool(first_name_pattern.match(components[1]))
        if not is_correct_first_name:
            raise CommandSyntaxError
        self.first_name = components[0]
        last_name_pattern = re.compile("[A-Za-z]{2,40}")
        is_correct_last_name = bool(last_name_pattern.match(components[2]))
        if not is_correct_last_name:
            raise CommandSyntaxError
        self.last_name = components[1]

        position_pattern = re.compile("[A-Za-z]{3,40}")
        is_correct_position = bool(position_pattern.match(components[2]))
        if not is_correct_position:
            raise CommandSyntaxError
        self.position = components[2]


class EditEmployeeCommandParser(Parser):
    def __init__(self, user_input):
        self.user_input = user_input
        self.number_of_arguments = 4
        self.arguments = []
        self.first_name = ""
        self.last_name = ""
        self.position = ""
        self.identifier = 0

    def parse(self):
        components = self.user_input.split()
        components.pop(0)
        if len(components) == 0 or len(components) > self.number_of_arguments:
            raise CommandSyntaxError

        try:
            self.identifier = int(components[0])
        except ValueError:
            raise CommandSyntaxError

        first_name_pattern = re.compile("[A-Za-z]{2,25}")
        is_correct_first_name = bool(first_name_pattern.match(components[1]))
        if not is_correct_first_name:
            raise CommandSyntaxError
        self.first_name = components[1]
        last_name_pattern = re.compile("[A-Za-z]{2,40}")
        is_correct_last_name = bool(last_name_pattern.match(components[2]))
        if not is_correct_last_name:
            raise CommandSyntaxError
        self.last_name = components[2]

        position_pattern = re.compile("[A-Za-z]{2,40}")
        is_correct_position = bool(position_pattern.match(components[3]))
        if not is_correct_position:
            raise CommandSyntaxError
        self.position = components[3]



