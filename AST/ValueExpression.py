from .Expression import Expression
from lib import Value, NumberValue, StringValue, Function, FunctionValue


class ValueExpression(Expression):
    def __init__(self, value: float | str | Function):
        if isinstance(value, float):
            self.value = NumberValue(value)
        elif isinstance(value, str):
            self.value = StringValue(value)
        elif isinstance(value, Function):
            self.value = FunctionValue(value)
    
    def __str__(self):
        return self.value.as_string()
    
    def eval(self) -> Value:
        return self.value
