from .Statement import Statement
from .Expression import Expression


class IfStatement(Statement):
    def __init__(self, expression: Expression, if_statement: Statement, else_statement: Statement | None):
        self.expression = expression
        self.if_statement = if_statement
        self.else_statement = else_statement

    def __str__(self):
        result: str = f'if {self.expression} {self.if_statement}'
        if self.else_statement is not None:
            result += f'\nelse {self.else_statement}'
        return result

    def execute(self):
        result: float = self.expression.eval().as_number()
        if result != 0:
            self.if_statement.execute()
        elif self.else_statement is not None:
            self.else_statement.execute()
