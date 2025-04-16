class User:
    def __init__(self, id, name, email, user_type):
        self.id = id
        self.name = name
        self.email = email
        self.user_type = user_type

    def to_dict(self):
        return vars(self)

    @staticmethod
    def from_dict(data):
        return User(**data)
