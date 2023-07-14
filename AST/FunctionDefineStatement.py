from .Statement import Statement
from lib import Functions, UserDefineFunction


class FunctionDefineStatement(Statement):
    def __init__(self, name: str, args_names: list[str], body: Statement):
        self.name = name
        self.args_names = args_names
        self.body = body

    def __str__(self):
        return f'function {self.name}({",".join(self.args_names)}) {str(self.body)}'

    def execute(self):
        Functions.set(self.name, UserDefineFunction(self.args_names, self.body))
