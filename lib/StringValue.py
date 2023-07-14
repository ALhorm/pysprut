from .Value import Value
from exceptions import Error


class StringValue(Value):
    def __init__(self, value: str):
        self.value = value

    def __repr__(self):
        return self.value

    def as_number(self):
        try:
            return float(self.value)
        except ValueError:
            Error('Cannot convert string to number.').call()

    def as_string(self):
        return self.value

    def as_array(self):
        return [char for char in self.value]
