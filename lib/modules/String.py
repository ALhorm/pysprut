from lib import Functions, Function, Value, StringValue, NumberValue, ArrayValue, DictionaryValue, FunctionValue
from .Module import Module
from exceptions import Error

STRING: str = ''


class SplitByFunction(Function):
    def execute(self, args: list[Value]) -> Value:
        if len(args) > 1:
            Error('The function takes only 1 argument.').call()
        global STRING
        return ArrayValue([StringValue(i) for i in STRING.split(args[0].as_string())])


class FindFunction(Function):
    def __init__(self, find_type: str):
        self.type = find_type

    def execute(self, args: list[Value]) -> Value:
        if len(args) > 1:
            Error('The function takes only 1 argument.').call()
        global STRING
        finder = STRING.find(args[0].as_string())
        match self.type:
            case 'index':
                return NumberValue(int(finder))
            case 'char':
                return StringValue(STRING[finder]) if finder != -1 else NumberValue(-1)


class UpperLowerFunction(Function):
    def __init__(self, case: str):
        self.case = case

    def execute(self, args: list[Value]) -> Value:
        if len(args) > 0:
            Error('The function does not accept any arguments.').call()
        global STRING
        match self.case:
            case 'upper':
                return StringValue(STRING.upper())
            case 'lower':
                return StringValue(STRING.upper())


class ClearFunction(Function):
    def execute(self, args: list[Value]) -> Value:
        if len(args) > 0:
            Error('The function does not accept any arguments.').call()
        return StringValue(args[0].as_string().strip())


class StringFunction(Function):
    def execute(self, args: list[Value]) -> Value:
        if len(args) > 1:
            raise Exception('The function takes only 1 argument.')
        global STRING
        STRING = args[0].as_string()
        return DictionaryValue({
            StringValue('splitBy'): FunctionValue(SplitByFunction()),
            StringValue('findIndex'): FunctionValue(FindFunction('index')),
            StringValue('findChar'): FunctionValue(FindFunction('char')),
            StringValue('toUpper'): FunctionValue(UpperLowerFunction('upper')),
            StringValue('toLower'): FunctionValue(UpperLowerFunction('lower')),
            StringValue('clear'): FunctionValue(ClearFunction()),
            StringValue('length'): NumberValue(len(STRING)),
            StringValue('text'): StringValue(STRING)
        })


class String(Module):
    functions: dict[str, Function] = {
        'String': StringFunction()
    }
    variables: dict[str, Value] = {}

    def init(self):
        for f in String.functions:
            Functions.set(f, String.functions[f])
