from ConsoleDBManager.command import Command


class CommandListController:
    def __init__(self):
        add = Command("add_dep", "add_department")
        select = Command("select_dep", "select_department")
        self.commands_list = [add, select]

    def __str__(self):
        description = ""
        for command in self.commands_list:
            description += command.text_description()
        return description
