from enum import Enum


class Command(Enum):
    ADD_DEPARTMENT = "add_department"
    SELECT_DEPARTMENT = "select_department"
    LIST_DEPARTMENT = "list_department"
    LIST_EMPLOYEE = "list_employee"
    ADD_EMPLOYEE = "add_employee"
    DELETE_EMPLOYEE = "delete_employee"
    EDIT_EMPLOYEE = "edit_employee"
    BACK = "back"


class MenuItem:
    def __init__(self, identifier, name, description, syntax, parent_id):
        self.id = identifier
        self.name = name
        self.description = description
        self.parent_id = parent_id
        self.syntax = syntax

    def text_description(self):
        return "{} {} {}".format(self.id, self.name, self.description)

    def visual_representation(self):
        components = [self.name]
        if len(self.syntax) != 0:
            components.append(self.syntax)
        components.append(self.description)
        return " - ".join(components)

    def __str__(self):
        return self.text_description()
