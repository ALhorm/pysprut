from lib import Value, ArrayValue
from .Expression import Expression


class ArrayExpression(Expression):
    def __init__(self, elements: list[Expression]):
        self.elements = elements

    def __repr__(self):
        return str(self.elements)

    def eval(self) -> Value:
        return ArrayValue([e.eval() for e in self.elements])
