from .Value import Value
from exceptions import Error


class NumberValue(Value):
    def __init__(self, value: float):
        self.value = value

    def __repr__(self):
        return self.as_string()

    def as_number(self):
        return self.value

    def as_string(self):
        return str(self.value)

    def as_array(self):
        Error('Cannot convert int to array.').call()
