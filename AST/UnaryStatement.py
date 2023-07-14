from .Statement import Statement
from lib import Variables, NumberValue, Value


class UnaryStatement(Statement):
    def __init__(self, variable: str, operation: str):
        self.variable = variable
        self.operation = operation

    def execute(self):
        variable: Value = Variables.get(self.variable)
        match self.operation:
            case '++':
                Variables.set(self.variable, NumberValue(variable.as_number() + 1))
            case '--':
                Variables.set(self.variable, NumberValue(variable.as_number() - 1))
