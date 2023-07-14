from .Statement import Statement
from .Expression import Expression
from .BreakStatement import BreakStatement
from .ContinueStatement import ContinueStatement


class DoWhileStatement(Statement):
    def __init__(self, condition: Expression, statement: Statement):
        self.condition = condition
        self.statement = statement

    def __str__(self):
        return f'do {self.statement} while {self.condition}'

    def execute(self):
        while True:
            try:
                self.statement.execute()
            except BreakStatement:
                break
            except ContinueStatement:
                pass
            if self.condition.eval().as_number() == 0:
                break
