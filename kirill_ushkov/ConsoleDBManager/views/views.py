from ..controllers.menu_controller import View
from ..models.menu_item import Command
from ..validators.validators import CommandValidator
from ..validators.errors import InputError
from ..parsers.command_parser import CommandParser, AddEmployeeCommandParser, EditEmployeeCommandParser
import logging

log_file_name = "app.log"
logger = logging.getLogger(log_file_name)
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler(log_file_name)
formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(name)s : %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


class MenuInitialView(View):

    def start(self):
        print("--------------------")
        menu_items = self.controller.dbController.get_initial_menu_items()
        for command in menu_items:
            print(command.visual_representation())

    def get_user_input(self):
        user_input = input("Please enter command:\n")
        return user_input.strip().lower()

    def handle_user_input(self, user_input):
        try:
            parser = CommandParser(user_input)
            parser.parse()
            menu_item = self.controller.dbController.get_selected_menu_item(parser.command)
            if menu_item is None:
                self.show_error_message()
            elif menu_item.name == Command.LIST_DEPARTMENT.value:
                view = DepartmentListView()
                self.controller.transition_to(view)
                logger.info("List department command selected")
            elif menu_item.name == Command.ADD_DEPARTMENT.value:
                view = AddNewDepartmentView(menu_item)
                self.controller.transition_to(view)
                logger.info("Add department command selected")
            elif menu_item.name == Command.SELECT_DEPARTMENT.value:
                if len(parser.arguments) == 0:
                    logger.error("Incorrect select department arguments")
                    raise InputError("Name argument not found", "Please enter department name")

                department = self.controller.dbController.get_department_by_name(parser.arguments[0])
                if department is None:
                    message = "No department with this name".format(parser.arguments[0])
                    print(message)
                    logger.info(message)
                    return
                view = SelectedDepartmentMenuView(menu_item, department)
                logger.info("Choose department command selected")
                self.controller.transition_to(view)
        except InputError as error:
            print(error.expression)
            print(error.message)
            logger.error("Initial menu error")

    def show_error_message(self):
        print("Unrecognized command! Please try again.")


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
            logger.info("Back to initial menu from department list")
        else:
            self.show_error_message()

    def get_user_input(self):
        user_input = input("Press B to return to previous menu:\n")
        return user_input.strip().lower()

    def show_error_message(self):
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
            logger.info("Back to initial menu from add department")
        except InputError as err:
            print(err.expression)
            print(err.message)
            logger.error("AddNewDepartmentView: {}".format(err.expression))

    def get_user_input(self):
        return input("Enter command:\n")

    def show_error_message(self):
        print("Incorrect command syntax!")


class SelectedDepartmentMenuView(View):
    def __init__(self, menu_item, department):
        self.department = department
        self.parent_menu_item = menu_item

    def start(self):
        print("------------------------------")
        print("Selected department - {}".format(self.department.name))
        print("Available commands")
        menu_items = self.controller.dbController.get_child_menu_items(self.parent_menu_item.id)
        for item in menu_items:
            print(item.visual_representation())

    def handle_user_input(self, user_input):
        try:
            parser = CommandParser(user_input)
            parser.parse()

            if parser.command == Command.LIST_EMPLOYEE.value:
                logger.info("List employee command selected")
                employees = self.controller.dbController.get_employees_for_department(self.department.identifier)
                view = ListEmployeesView(employees, self.department, self.parent_menu_item)
                self.controller.transition_to(view)
            elif parser.command == Command.ADD_EMPLOYEE.value:
                logger.info("Add employee command selected")
                command_parser = AddEmployeeCommandParser(user_input)
                command_parser.parse()
                self.controller.dbController.add_employee(command_parser.first_name,
                                                          command_parser.last_name,
                                                          command_parser.position,
                                                          self.department.identifier)
                print("Successfully added employee!")
            elif parser.command == Command.BACK.value:
                logger.info("Back to initial from selected department")
                view = MenuInitialView()
                self.controller.transition_to(view)
            elif parser.command == Command.DELETE_EMPLOYEE.value:
                logger.info("Delete employee command selected")
                employee_id = parser.arguments[0]
                self.controller.dbController.remove_employee(employee_id, self.department.identifier)
                print("Successfully deleted employee profile!")
            elif parser.command == Command.EDIT_EMPLOYEE.value:
                command_parser = EditEmployeeCommandParser(user_input)
                command_parser.parse()
                self.controller.dbController.edit_employee(command_parser.identifier,
                                                           command_parser.first_name,
                                                           command_parser.last_name,
                                                           command_parser.position)
                print("Successfully updated employee profile!")
            else:
                self.show_error_message()
        except InputError as error:
            print(error.expression)
            print(error.message)
            logger.error("SelectedDepartmentMenuView: {}".format(error.expression))

    def get_user_input(self):
        return input("Enter command:\n").strip()

    def show_error_message(self):
        print("Unrecognized command!\n")


class ListEmployeesView(View):
    def __init__(self, employees, department, parent_menu_item):
        self.department = department
        self.parent_menu = parent_menu_item
        self.employees = employees

    def start(self):
        print("List of employees in {} department".format(self.department.name))
        for emp in self.employees:
            print(emp)

    def handle_user_input(self, user_input):
        if user_input == "b":
            logger.info("Back to selected view from employees list")
            view = SelectedDepartmentMenuView(self.parent_menu, self.department)
            self.controller.transition_to(view)

    def get_user_input(self):
        user_input = input("Press B to return to previous menu:\n")
        return user_input.strip().lower()

    def show_error_message(self):
        print("Unrecognized command!\n")
