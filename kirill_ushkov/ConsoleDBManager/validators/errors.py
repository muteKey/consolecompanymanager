class Error(Exception):
    pass


class CommandSyntaxError(Error):
    pass


class CommandMismatchError(Error):
    pass


class TooShortDepartmentNameError(Error):
    pass


