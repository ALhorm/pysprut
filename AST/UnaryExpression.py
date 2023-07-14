from .Expression import Expression
from lib import Value, NumberValue


class UnaryExpression(Expression):
    def __init__(self, operation: str, expr: Expression):
        self.operation = operation
        self.expr = expr
    
    def __str__(self):
        return self.operation + str(self.expr)
    
    def eval(self) -> Value:
        match self.operation:
            case '+':
                return self.expr.eval()
            case '-':
                return NumberValue(-self.expr.eval().as_number())
