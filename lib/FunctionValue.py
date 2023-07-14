from .Value import Value
from .Function import Function
from exceptions import Error


class FunctionValue(Value):
    def __init__(self, value: Function):
        self.value = value

    def as_number(self):
        Error('Cannot convert function to number.').call()

    def as_string(self):
        return str(self.value)

    def as_array(self):
        Error('Cannot convert function to array.').call()
