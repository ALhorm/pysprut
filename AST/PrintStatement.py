from .Statement import Statement
from .Expression import Expression


class PrintStatement(Statement):
    def __init__(self, expression: Expression, new_line: bool = False):
        self.expression = expression
        self.new_line = new_line

    def __str__(self):
        if self.new_line:
            return f'println {self.expression}'
        else:
            return f'print {self.expression}'

    def execute(self):
        if self.new_line:
            print(self.expression.eval())
        else:
            print(self.expression.eval(), end='')
