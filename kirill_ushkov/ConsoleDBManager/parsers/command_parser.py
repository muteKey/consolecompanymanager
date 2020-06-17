from ..validators.errors import CommandSyntaxError


class CommandParser:
    def __init__(self, user_input):
        self.user_input = user_input

    def parse(self):
        commands = self.user_input.split()
        if len(commands) < 2 or len(commands) > 2:
            raise CommandSyntaxError
        return commands
