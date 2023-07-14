from .Value import Value
from exceptions import Error


class ArrayValue(Value):
    def __init__(self, elements: list[Value]):
        self.elements = elements.copy()

    def __repr__(self):
        return self.as_string()

    def get(self, index: int):
        return self.elements[index]

    def set(self, index: int, value: Value):
        self.elements[index] = value

    def as_number(self):
        Error('Cannot convert function to number.').call()

    def as_string(self):
        return str(self.elements)

    def as_array(self):
        return self.elements
