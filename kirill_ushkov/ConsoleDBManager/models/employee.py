class Employee:
    def __init__(self, identifier, first_name, last_name, position, department_id):
        self.identifier = identifier
        self.first_name = first_name
        self.last_name = last_name
        self.position = position
        self.department_id = department_id

    def visual_repr(self):
        return "{} {} {}".format(self.first_name, self.last_name, self.position)

    def __str__(self):
        return "{} {} {} {}".format(self.identifier, self.first_name, self.last_name, self.position)
