from .Statement import Statement
from .FunctionalExpression import FunctionalExpression


class FunctionStatement(Statement):
    def __init__(self, function: FunctionalExpression):
        self.function = function

    def __str__(self):
        return str(self.function)

    def execute(self):
        self.function.eval()
