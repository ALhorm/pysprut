from .Function import Function
from .Value import Value
from .NumberValue import NumberValue
from .StringValue import StringValue
from .ArrayValue import ArrayValue
from .DictionaryValue import DictionaryValue
from sys import exit
from time import sleep


class PrintfFunction(Function):
    def execute(self, args: list[Value]):
        for arg in args:
            print(arg, end='')


class GetFunction(Function):
    def __init__(self, input_type: str):
        self.type = input_type

    def execute(self, args: list[Value]) -> Value:
        if len(args) > 1:
            raise Exception('The function takes only 1 argument.')
        text: str = ''
        if len(args) == 1:
            text = args[0].as_string()
        elif len(args) == 0:
            text = ''
        match self.type:
            case 'int':
                return NumberValue(int(input(text)))
            case 'float':
                return NumberValue(float(input(text)))
            case 'string':
                return StringValue(input(text))


class ArrayFunction(Function):
    def execute(self, args: list[Value]) -> Value:
        return ArrayValue(args)


class ToTypeFunction(Function):
    def __init__(self, target_type: str):
        self.type = target_type

    def execute(self, args: list[Value]) -> Value:
        if len(args) > 1:
            raise Exception('The function takes only 1 argument.')
        value = args[0].as_string()
        match self.type:
            case 'int':
                return NumberValue(int(float(value)))
            case 'float':
                return NumberValue(float(value))
            case 'string':
                return StringValue(value)
            case 'array':
                return ArrayValue(args[0].as_array())


class TypeOfFunction(Function):
    def execute(self, args: list[Value]) -> Value:
        if len(args) > 1:
            raise Exception('The function takes only 1 argument.')
        if isinstance(args[0], StringValue):
            return StringValue('string')
        elif isinstance(args[0], ArrayValue):
            return StringValue('array')
        elif isinstance(args[0], DictionaryValue):
            return StringValue('dict')
        elif isinstance(args[0].as_number(), int):
            return StringValue('int')
        elif isinstance(args[0].as_number(), float):
            return StringValue('float')


class ExitFunction(Function):
    def execute(self, args: list[Value]):
        if len(args) > 0:
            raise Exception('The function does not accept any arguments.')
        exit(1)


class SleepFunction(Function):
    def execute(self, args: list[Value]):
        if len(args) > 1:
            raise Exception('The function takes only 1 argument.')
        sleep(args[0].as_number())


class Functions:
    functions: dict[str, Function] = {
        'printf': PrintfFunction(),
        'getInt': GetFunction('int'),
        'getFloat': GetFunction('float'),
        'getString': GetFunction('string'),
        'toInt': ToTypeFunction('int'),
        'toFloat': ToTypeFunction('float'),
        'toString': ToTypeFunction('string'),
        'toArray': ToTypeFunction('array'),
        'typeOf': TypeOfFunction(),
        'exit': ExitFunction(),
        'sleep': SleepFunction()
    }

    @staticmethod
    def is_exists(key: str) -> bool:
        return key in Functions.functions

    @staticmethod
    def get(key: str) -> Function:
        if not Functions.is_exists(key):
            raise Exception('Unknown function.')
        return Functions.functions[key]

    @staticmethod
    def set(key: str, value: Function):
        Functions.functions[key] = value
