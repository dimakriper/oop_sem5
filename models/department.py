class Department:
    def __init__(self, id, name):
        self._id = id
        self._name = name

    # Getter methods for Department attributes
    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name
