from .Value import Value
from .StringValue import StringValue
from exceptions import Error


class DictionaryValue(Value):
    def __init__(self, dictionary: dict[StringValue, Value]):
        self.dictionary = dictionary.copy()

    def __repr__(self):
        return self.as_string()

    def get(self, key: StringValue):
        for i in self.dictionary.items():
            if i[0].value == key.value:
                return i[1]

    def set(self, key: StringValue, value: Value):
        for i in self.dictionary.items():
            if i[0].value == key.value:
                self.dictionary[i[0]] = value
                return
        self.dictionary[key] = value

    def as_number(self):
        Error('Cannot convert function to number.').call()

    def as_string(self):
        return str(self.dictionary)

    def as_array(self):
        Error('Cannot convert function to array.').call()
