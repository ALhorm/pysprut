from .Statement import Statement


class ContinueStatement(Statement, Exception):
    def __str__(self):
        return 'continue'

    def execute(self):
        raise self
