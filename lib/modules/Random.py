from lib import Functions, Function, Value, NumberValue, StringValue
from .Module import Module
from exceptions import Error
import random
from string import printable


class RandomFunction(Function):
    def __init__(self, random_type: str):
        self.type = random_type

    def execute(self, args: list[Value]) -> Value:
        if len(args) > 2:
            Error('The function takes only 2 arguments.').call()
        match self.type:
            case 'int':
                return NumberValue(random.randint(args[0].as_number(), args[1].as_number()))
            case 'float':
                return NumberValue(random.uniform(args[0].as_number(), args[1].as_number()))
            case 'char':
                if len(args) > 0:
                    Error('The function does not accept any arguments.').call()
                return StringValue(random.choice(printable[:-6]))


class RandomFromFunction(Function):
    def execute(self, args: list[Value]) -> Value:
        if len(args) > 1:
            Error('The function takes only 1 argument.').call()
        return StringValue(str(random.choice(args[0].as_array())))


class Random(Module):
    functions: dict[str, Function] = {
        'randomInt': RandomFunction('int'),
        'randomFloat': RandomFunction('float'),
        'randomChar': RandomFunction('char'),
        'randomFrom': RandomFromFunction()
    }
    variables: dict[str, Value] = {}

    def init(self):
        for f in Random.functions:
            Functions.set(f, Random.functions[f])
