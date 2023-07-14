from .Statement import Statement
from AST import Expression
from .AccessExpression import AccessExpression
from lib import Value, Variables, ArrayValue, StringValue


class ArrayAssignmentStatement(Statement):
    def __init__(self, array: AccessExpression, expression: Expression):
        self.array = array
        self.expression = expression

    def __repr__(self):
        return f'{self.array} = {self.expression}'

    def execute(self):
        container: Value = Variables.get(self.array.variable)
        if isinstance(container, ArrayValue):
            last_index: int = int(self.array.last_index().as_number())
            self.array.get_array().set(last_index, self.expression.eval())
            return
        self.array.get_dictionary().set(StringValue(self.array.last_index().as_string()), self.expression.eval())
