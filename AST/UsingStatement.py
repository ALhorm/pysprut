from .Statement import Statement
from .Expression import Expression
from importlib import import_module
from lib import Functions, Variables


class UsingStatement(Statement):
    def __init__(self, expression: Expression, values: dict[str, str]):
        self.expression = expression
        self.values = values

    def execute(self):
        try:
            module_name: str = self.expression.eval().as_string()
            module = import_module(f'lib.modules.{module_name}')
            module_class = dict([(name, cls) for name, cls in module.__dict__.items() if isinstance(cls, type)])
            if len(self.values) == 0:
                module_class[module_name]().init()
            else:
                for f in self.values:
                    if f in module_class[module_name]().functions:
                        Functions.set(self.values[f] if self.values[f] != '' else f, module_class[module_name]().functions[f])
                    if f in module_class[module_name]().variables:
                        Variables.set(self.values[f] if self.values[f] != '' else f, module_class[module_name]().variables[f])
        except Exception:
            pass
