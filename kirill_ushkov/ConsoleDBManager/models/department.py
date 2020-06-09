
class Department:
    def __init__(self, identifier, name):
        self.identifier = identifier
        self.name = name

    def __str__(self):
        return "{} {}".format(self.identifier, self.name)
