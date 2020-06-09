from ..views.menu_view import MenuView
from .database_controller import DatabaseController


class MenuController:
    def __init__(self):
        self.dbController = DatabaseController()
        menu_items = self.dbController.get_initial_menu_items()
        self.view = MenuView(menu_items)

    def start_lifecycle(self):
        self.view.display()
        user_input = self.view.get_user_input()
        validated = self.validate_input(user_input)

        menu_item = self.dbController.get_selected_menu_item(validated)
        if menu_item is not None:
            self.view.display_command_syntax(menu_item)
            menu_items = self.dbController.get_child_menu_items(menu_item.id)
            if len(menu_items) > 0:
                self.view = MenuView(menu_items)
                self.start_lifecycle()
            else:
                print("no child menu commands")
        else:
            self.view.display_unrecognized_command_error()

    def validate_input(self, user_input):
        return user_input.strip().lower()

