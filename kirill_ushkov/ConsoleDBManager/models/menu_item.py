

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
        return "{} - {}".format(self.id, self.description)

    def __str__(self):
        return self.text_description()
