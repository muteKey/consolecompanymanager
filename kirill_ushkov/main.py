from ConsoleDBManager.controllers.menu_controller import MenuController
from ConsoleDBManager.views.views import MenuInitialView

try:
    menuController = MenuController(MenuInitialView())
except KeyboardInterrupt:
    print()
    print("Goodbye!")
