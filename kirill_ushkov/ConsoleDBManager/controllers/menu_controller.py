from ConsoleDBManager.views.menu_view import MenuView
from ConsoleDBManager.models.menu_state import MenuItem
from ConsoleDBManager.models.command import Command


class MenuController:
    def __init__(self):
        commands = [Command.add_department_command(),
                    Command.select_department_command(),
                    Command.quit_command()]
        self.view = MenuView(MenuItem.DepartmentSelection, commands)

    def start_lifecycle(self):
        self.view.display()
        user_input = self.view.get_user_input()
        validated = self.validate_input(user_input)

        command = self.view.get_selected_command(validated)
        if command is not None:
            self.view = self.get_view_for_command(command)
            self.start_lifecycle()
        else:
            self.view.display_unrecognized_command_error()

    def validate_input(self, user_input):
        return user_input.strip().lower()

    def handle_command(self, command):
        if command == Command.select_department_command():
            print()

    def get_view_for_command(self, command):
        if command == Command.select_department_command():
            commands = [Command.list_employee_command(),
                        Command.add_new_employee_command(),
                        Command.delete_employee_command(),
                        Command.edit_employee_command(),
                        Command.back_command()]
            return MenuView(MenuItem.DepartmentSelected, commands)
        elif command == Command.back_command():
            commands = [Command.add_department_command(),
                        Command.select_department_command(),
                        Command.quit_command()]
            return MenuView(MenuItem.DepartmentSelection, commands)
        elif command == Command.edit_employee_command():

