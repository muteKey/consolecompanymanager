class Command:
    def __init__(self, command_name, description, syntax=None):
        self.command_name = command_name
        self.description = description
        self.syntax = syntax

    def __str__(self):
        return self.text_description()

    def text_description(self):
        result = ""
        result += self.command_name
        if self.syntax is not None:
            result += "\n"
            result += "Syntax: "
            result += self.syntax
        result += " - "
        result += self.description

        return result

    def __eq__(self, other):
        if not isinstance(other, Command):
            return False
        return self.command_name == other.command_name

    @classmethod
    def add_department_command(cls):
        return cls("add_department",
                   "creates department with <department_name>",
                   "add_department <department_name>")

    @classmethod
    def select_department_command(cls):
        return cls("select_department",
                   "selects department with <department_name>",
                   "select_department <department_name>")

    @classmethod
    def quit_command(cls):
        return cls("quit", "actually quits program :)")

    @classmethod
    def list_employee_command(cls):
        return cls("list_employee", "gets list of employee of selected department")

    @classmethod
    def add_new_employee_command(cls):
        return cls("add_employee",
                   "adds new employee to selected department",
                   "add_employee name last_name position")

    @classmethod
    def delete_employee_command(cls):
        return cls("delete_employee",
                   "deletes employee from selected department by specified id",
                   "delete_employee employee_id")

    @classmethod
    def edit_employee_command(cls):
        return cls("edit_employee",
                   "updates profile of employee from selected department by specified id",
                   "edit_employee employee_id name last_name position")

    @classmethod
    def back_command(cls):
        return cls("back", "get back to department selection menu")
