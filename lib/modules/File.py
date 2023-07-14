from lib import Functions, Function, Value, StringValue, ArrayValue, DictionaryValue, FunctionValue
from .Module import Module
from os.path import isfile
from exceptions import Error

FILE: str = ''


class ReadFileFunction(Function):
    def __init__(self, mode: str):
        self.mode = mode

    def execute(self, args: list[Value]) -> Value:
        if len(args) > 0:
            Error('The function does not accept any arguments.').call()
        global FILE
        if not isfile(FILE):
            Error('The file was not found.').call()
        with open(FILE, 'r') as f:
            match self.mode:
                case 'all':
                    return StringValue(f.read())
                case 'lines':
                    return ArrayValue([StringValue(i) for i in f.readlines()])


class WriteFileFunction(Function):
    def __init__(self, mode: str):
        self.mode = mode

    def execute(self, args: list[Value]):
        if len(args) > 1:
            Error('The function takes only 1 argument.').call()
        global FILE
        with open(FILE, self.mode) as f:
            f.write(args[0].as_string())


class OpenFileFunction(Function):
    def execute(self, args: list[Value]) -> Value:
        if len(args) > 1:
            Error('The function takes only 1 argument.').call()
        global FILE
        FILE = args[0].as_string()
        return DictionaryValue({
            StringValue('read'): FunctionValue(ReadFileFunction('all')),
            StringValue('readLines'): FunctionValue(ReadFileFunction('lines')),
            StringValue('write'): FunctionValue(WriteFileFunction('w')),
            StringValue('add'): FunctionValue(WriteFileFunction('a'))
        })


class File(Module):
    functions: dict[str, Function] = {
        'File': OpenFileFunction()
    }
    variables: dict[str, Value] = {}

    def init(self):
        for f in File.functions:
            Functions.set(f, File.functions[f])
