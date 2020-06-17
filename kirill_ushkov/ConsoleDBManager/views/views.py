from ..controllers.menu_controller import View
from ..models.menu_item import Command
from ..validators.validators import CommandValidator
from ..validators.errors import CommandMismatchError, CommandSyntaxError, TooShortDepartmentNameError
from ..parsers.command_parser import CommandParser


class MenuInitialView(View):

    def start(self):
        print("Welcome to Console Company Manager!")
        menu_items = self.controller.dbController.get_initial_menu_items()
        for command in menu_items:
            print(command.visual_representation())

    def get_user_input(self):
        user_input = input("Please enter command:\n")
        return user_input.strip().lower()

    def handle_user_input(self, user_input):
        try:
            parser = CommandParser(user_input)
            commands = parser.parse()
            menu_item = self.controller.dbController.get_selected_menu_item(commands[0])
            if menu_item.name == Command.LIST_DEPARTMENT.value:
                view = DepartmentListView()
                self.controller.transition_to(view)
            elif menu_item.name == Command.ADD_DEPARTMENT.value:
                view = AddNewDepartmentView(menu_item)
                self.controller.transition_to(view)
            elif menu_item.name == Command.SELECT_DEPARTMENT.value:
                department = self.controller.dbController.get_department_by_name(commands[1])
                view = SelectedDepartmentMenuView(menu_item, department)
                self.controller.transition_to(view)
        except CommandSyntaxError:
            self.show_error()

    def show_error(self):
        print("Unrecognized command error")


class DepartmentListView(View):

    def start(self):
        print("Showing list of available departments")
        departments = self.controller.dbController.get_all_departments()
        for dep in departments:
            print(dep)

    def handle_user_input(self, user_input):
        if user_input == "b":
            view = MenuInitialView()
            self.controller.transition_to(view)
        else:
            self.show_error()

    def get_user_input(self):
        user_input = input("Press B to return to previous menu:\n")
        return user_input.strip().lower()

    def show_error(self):
        print("Sorry, did not understand you, please try again")


class AddNewDepartmentView(View):
    def __init__(self, menu_item):
        self.menu_item = menu_item

    def start(self):
        print(self.menu_item.description)
        print("Command syntax: {}".format(self.menu_item.syntax))

    def handle_user_input(self, user_input):
        cleared = user_input.strip()
        try:
            validator = CommandValidator(Command.ADD_DEPARTMENT)
            dep_name = validator.validate(cleared)
            self.controller.dbController.add_department(dep_name)

            print("Successfully added new department!")
            view = MenuInitialView()
            self.controller.transition_to(view)
        except TooShortDepartmentNameError:
            print("Name of department is too short! Please try again")
            print()
        except CommandMismatchError:
            print("Please check your syntax. Seems like incorrect command entered")
            print()
        except CommandSyntaxError:
            print("Please check command syntax")

    def get_user_input(self):
        return input("Enter command:\n")

    def show_error(self):
        print("Incorrect command syntax!")


class SelectedDepartmentMenuView(View):
    def __init__(self, menu_item, department):
        self.department = department
        self.parent_menu_item = menu_item

    def start(self):
        print("Selected department - {}".format(self.department.name))
        print("Available commands")
        menu_items = self.controller.dbController.get_child_menu_items(self.parent_menu_item.id)
        for item in menu_items:
            print(item.visual_representation())

    def handle_user_input(self, user_input):
        print(user_input)

    def get_user_input(self):
        return input("Enter command:\n")

    def show_error(self):
        pass