from .Statement import Statement
from .Expression import Expression
from .BreakStatement import BreakStatement
from .ContinueStatement import ContinueStatement


class WhileStatement(Statement):
    def __init__(self, condition: Expression, statement: Statement):
        self.condition = condition
        self.statement = statement

    def __str__(self):
        return f'while {self.condition} {self.statement}'

    def execute(self):
        while self.condition.eval().as_number() != 0:
            try:
                self.statement.execute()
            except BreakStatement:
                break
            except ContinueStatement:
                pass
