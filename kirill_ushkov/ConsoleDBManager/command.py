class Command:
    def __init__(self, command_type, display_name):
        self.command_type = command_type
        self.display_name = display_name

    def __str__(self):
        return self.text_description()

    def text_description(self):
        return self.display_name
