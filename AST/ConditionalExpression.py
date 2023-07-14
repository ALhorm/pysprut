from .Expression import Expression
from lib import Value, NumberValue, StringValue
from enum import Enum


class Operator(Enum):
    PLUS = r'\+'
    MINUS = r'\-'
    MULTIPLY = r'\*'
    DIVIDE = r'/'

    EQUALS = r'=='
    GREATER = r'>'
    GREATER_ASSIGN = r'>='
    LESS = r'<'
    LESS_ASSIGN = r'<='
    REJECT = r'!'
    REJECT_ASSIGN = r'!='
    AND = r'&&'
    OR = r'||'


class ConditionalExpression(Expression):
    def __init__(self, operation: Operator, expr1: Expression, expr2: Expression):
        self.expr1 = expr1
        self.expr2 = expr2
        self.operation = operation

    def __str__(self):
        return f'({self.expr1} {self.operation.name} {self.expr2})'

    def eval(self) -> Value:
        value1: Value = self.expr1.eval()
        value2: Value = self.expr2.eval()

        number1: float = 0
        number2: float = 0
        if isinstance(value1, StringValue):
            number1 = value1.as_string()
            number2 = value2.as_string()
        else:
            number1 = value1.as_number()
            number2 = value2.as_number()

        result: bool = True
        match self.operation:
            case self.operation.EQUALS:
                result = number1 == number2
            case self.operation.GREATER:
                result = number1 > number2
            case self.operation.GREATER_ASSIGN:
                result = number1 >= number2
            case self.operation.LESS:
                result = number1 < number2
            case self.operation.LESS_ASSIGN:
                result = number1 <= number2
            case self.operation.REJECT_ASSIGN:
                result = number1 != number2
            case self.operation.AND:
                result = (number1 != 0) and (number2 != 0)
            case self.operation.OR:
                result = (number1 != 0) or (number2 != 0)
            case _:
                raise Exception('Unknown operation.')
        return NumberValue(int(result))
