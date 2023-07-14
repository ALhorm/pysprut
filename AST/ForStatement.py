from .Statement import Statement
from .Expression import Expression
from .BreakStatement import BreakStatement
from .ContinueStatement import ContinueStatement


class ForStatement(Statement):
    def __init__(self, initialization: Statement, condition: Expression, action: Statement, statement: Statement):
        self.initialization = initialization
        self.condition = condition
        self.action = action
        self.statement = statement

    def __str__(self):
        return f'for {self.initialization}, {self.condition}, {self.action} {self.statement}'

    def execute(self):
        self.initialization.execute()
        while self.condition.eval().as_number() != 0:
            try:
                self.statement.execute()
            except BreakStatement:
                break
            except ContinueStatement:
                pass
            self.action.execute()
