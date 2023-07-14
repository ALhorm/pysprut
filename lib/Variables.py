from .Value import Value
from .NumberValue import NumberValue


class Variables:
    variables: dict[str, Value] = {}
    stack: list[dict[str, Value]] = []
    ZERO: NumberValue = NumberValue(0)

    @staticmethod
    def push():
        Variables.stack.append(Variables.variables.copy())

    @staticmethod
    def pop():
        Variables.variables = Variables.stack.pop()
    
    @staticmethod
    def is_exists(key: str) -> bool:
        return key in Variables.variables
    
    @staticmethod
    def get(key: str) -> Value:
        if not Variables.is_exists(key):
            raise Exception(f'Unknown variable {key}.')
        return Variables.variables[key]

    @staticmethod
    def set(key: str, value: Value):
        Variables.variables[key] = value
