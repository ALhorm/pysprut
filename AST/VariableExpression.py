from .Expression import Expression
from lib import Variables, Value
from exceptions import UnknownVariableException


class VariableExpression(Expression):
    def __init__(self, name: str):
        self.name = name
    
    def __str__(self):
        return str(self.eval())
    
    def eval(self) -> Value:
        if not Variables.is_exists(self.name):
            raise UnknownVariableException(self.name)
        return Variables.get(self.name)
