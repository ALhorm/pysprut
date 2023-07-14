from .Statement import Statement
from .Expression import Expression
from lib import Variables, Value, NumberValue, StringValue, ArrayValue


class AssignmentStatement(Statement):
    def __init__(self, variable: str, expression: Expression, variable_type: str | None = None):
        self.variable = variable
        self.expression = expression
        self.type = variable_type

    def __str__(self):
        return f'{self.variable} = {self.expression}'

    def execute(self):
        result: Value | None = None
        match self.type:
            case None:
                result = self.expression.eval()
            case 'int':
                result = NumberValue(int(self.expression.eval().as_number()))
            case 'float':
                result = NumberValue(self.expression.eval().as_number())
            case 'string':
                result = StringValue(self.expression.eval().as_string())
            case 'array':
                result = ArrayValue(self.expression.eval().as_array())
            case _:
                raise Exception('Unknown type.')
        Variables.set(self.variable, result)
