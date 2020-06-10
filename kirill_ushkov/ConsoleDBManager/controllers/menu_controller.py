from __future__ import annotations
from .database_controller import DatabaseController
from abc import ABC, abstractmethod


class MenuController:
    _view = None

    def __init__(self, view) -> None:
        self.dbController = DatabaseController()
        self.transition_to(view)
        self.start_lifecycle()

    def transition_to(self, view: View):
        self._view = view
        self._view.controller = self

    def start_lifecycle(self):
        while True:
            self._view.start()
            user_input = self._view.get_user_input()
            self._view.handle_user_input(user_input)


class View(ABC):

    @property
    def controller(self) -> MenuController:
        return self._controller

    @controller.setter
    def controller(self, controller) -> None:
        self._controller = controller

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def handle_user_input(self, user_input):
        pass

    @abstractmethod
    def get_user_input(self):
        pass

    @abstractmethod
    def show_error(self):
        pass

    @abstractmethod
    def show_results(self):
        pass
