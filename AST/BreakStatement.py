from .Statement import Statement


class BreakStatement(Statement, Exception):
    def __str__(self):
        return 'break'

    def execute(self):
        raise self
