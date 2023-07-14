from .Statement import Statement
from AST import Expression
from lib import Value


class ReturnException(Exception):
    def __init__(self, value: Value):
        self.value = value


class ReturnStatement(Statement):
    def __init__(self, expression: Expression):
        self.expression = expression
        self.result: Value | None = None

    def __str__(self):
        return 'return'

    def execute(self):
        raise ReturnException(self.expression.eval())
