

class Role(metaclass=type):
    """
    Represents a role assigned to users.
    """

    def __init__(self, role_id, name):
        self.role_id = role_id
        self.name = name
        self.conditions = []

    def add_condition(self, condition):
        self.conditions.append(condition)

    def get_conditions(self):
        return self.conditions 
    