from ..controllers.menu_controller import View
from ..models.menu_item import Command


class MenuInitialView(View):

    def start(self):
        menu_items = self.controller.dbController.get_initial_menu_items()
        for command in menu_items:
            print(command.visual_representation())

    def get_user_input(self):
        user_input = input("Please enter number of command:\n")
        return user_input.strip().lower()

    def handle_user_input(self, user_input):
        menu_item = self.controller.dbController.get_selected_menu_item(user_input)
        if menu_item is not None:
            if menu_item.name == Command.LIST_DEPARTMENT.value:
                view = DepartmentListView()
                self.controller.transition_to(view)
            else:
                self.show_error()
        else:
            self.show_error()

    def show_error(self):
        print("Unrecognized command error")

    def show_results(self):
        pass


class DepartmentListView(View):

    def start(self):
        print("Showing list of available departments")
        departments = self.controller.dbController.get_all_departments()
        for dep in departments:
            print(dep)

    def handle_user_input(self, user_input):
        pass

    def get_user_input(self):
        user_input = input("Press B to return to previous menu:\n")
        return user_input.strip().lower()

    def show_error(self):
        pass

    def show_results(self):
        pass
