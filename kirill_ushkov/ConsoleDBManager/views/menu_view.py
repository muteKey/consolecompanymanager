
class MenuView:

    def __init__(self, menu_items):
        self.menu_items = menu_items

    def display(self):
        print("---------------------------")
        for command in self.menu_items:
            print(command.visual_representation())

    def display_command_syntax(self, menu_item):
        print("---------------------------")
        print("Syntax is: {}".format(menu_item.syntax))

    def get_user_input(self):
        return input("Please enter number of command:\n")

    def display_unrecognized_command_error(self):
        print("Unrecognized command!")

