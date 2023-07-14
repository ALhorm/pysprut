from .Statement import Statement


class BlockStatement(Statement):
    def __init__(self):
        self.statements: list[Statement] = []

    def __str__(self):
        result: str = ''
        for statement in self.statements:
            result += f'{statement}\n'
        return result

    def add(self, statement: Statement):
        self.statements.append(statement)

    def execute(self):
        for statement in self.statements:
            statement.execute()
