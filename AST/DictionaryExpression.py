from lib import Value, DictionaryValue
from .Expression import Expression


class DictionaryExpression(Expression):
    def __init__(self, elements: dict[Expression, Expression]):
        self.elements = elements

    def eval(self) -> Value:
        dictionary: DictionaryValue = DictionaryValue({})
        for key in self.elements:
            dictionary.set(key.eval(), self.elements[key].eval())
        return dictionary
