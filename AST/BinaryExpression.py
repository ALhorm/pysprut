from .Expression import Expression
from lib import Value, NumberValue, StringValue, ArrayValue


class BinaryExpression(Expression):
    def __init__(self, operation: str, expr1: Expression, expr2: Expression):
        self.expr1 = expr1
        self.expr2 = expr2
        self.operation = operation
    
    def __str__(self):
        return f'({self.expr1} {self.operation} {self.expr2})'
    
    def eval(self) -> Value:
        value1: Value = self.expr1.eval()
        value2: Value = self.expr2.eval()
        if isinstance(value1, StringValue) or isinstance(value1, ArrayValue):
            string: str = value1.as_string()
            match self.operation:
                case '+':
                    return StringValue(string + value2.as_string())
                case '*':
                    return StringValue(string * int(value2.as_number()))
                case '/':
                    return StringValue(string[:int(len(string) / value2.as_number())])

        number1: float = value1.as_number()
        number2: float = value2.as_number()
        match self.operation:
            case '+':
                return NumberValue(number1 + number2)
            case '-':
                return NumberValue(number1 - number2)
            case '*':
                return NumberValue(number1 * number2)
            case '/':
                return NumberValue(number1 / number2)
