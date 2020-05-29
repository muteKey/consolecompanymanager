
class MenuView:

    def __init__(self, menu_item, commands_list):
        self.menu_item = menu_item
        self.commands_list = commands_list

    def display(self):
        print("---------------------------")
        print("List of available commands:")
        for command in self.commands_list:
            print(command.text_description())

    def get_user_input(self):
        return input("Please enter command:\n")

    def display_unrecognized_command_error(self):
        print("Unrecognized command!")

    def get_selected_command(self, input_command):
        for command in self.commands_list:
            if command.command_name == input_command:
                return command
        return None

