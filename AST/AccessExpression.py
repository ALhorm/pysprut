from AST import Expression
from lib import Variables, Value, ArrayValue, DictionaryValue, StringValue


class AccessExpression(Expression):
    def __init__(self, variable: str, indices: list[Expression]):
        self.variable = variable
        self.indices = indices

    def __repr__(self):
        return self.variable + str(self.indices)

    def get_array(self) -> ArrayValue:
        array: ArrayValue = self.consume_array(Variables.get(self.variable))
        for i in range(len(self.indices) - 1):
            array = self.consume_array(array.get(int(self.index(i).as_number())))
            index: int = int(self.index(i).as_number())
            array = self.consume_array(array.get(index))
        return array

    def index(self, index: int) -> Value:
        return self.indices[index].eval()

    def last_index(self) -> Value:
        return self.index(len(self.indices) - 1)

    def get_dictionary(self) -> DictionaryValue:
        dictionary: DictionaryValue = self.consume_dictionary(Variables.get(self.variable))
        for i in range(len(self.indices) - 1):
            dictionary = self.consume_dictionary(dictionary.get(StringValue(self.index(i).as_string())))
        return dictionary

    @staticmethod
    def consume_array(value: Value) -> ArrayValue:
        if isinstance(value, ArrayValue):
            return value
        else:
            raise Exception('Array expected.')

    @staticmethod
    def consume_dictionary(value: Value) -> DictionaryValue:
        if isinstance(value, DictionaryValue):
            return value
        else:
            raise Exception('Dictionary expected.')

    def eval(self) -> Value:
        container: Value = Variables.get(self.variable)
        if isinstance(container, ArrayValue):
            return self.get_array().get(int(self.last_index().as_number()))
        return self.get_dictionary().get(StringValue(self.last_index().as_string()))
