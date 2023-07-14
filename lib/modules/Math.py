from lib import Functions, Function, Value, NumberValue, Variables
from .Module import Module
from exceptions import Error
import math


class FactorialFunction(Function):
    def execute(self, args: list[Value]) -> Value:
        if len(args) > 1:
            Error('The function takes only 1 argument.').call()
        return NumberValue(math.factorial(int(args[0].as_number())))


class RoundFunction(Function):
    def __init__(self, round_name: str):
        self.name = round_name

    def execute(self, args: list[Value]) -> Value:
        if len(args) > 1:
            Error('The function takes only 1 argument.').call()
        match self.name:
            case 'round':
                return NumberValue(round(args[0].as_number()))
            case 'roundUp':
                return NumberValue(math.ceil(args[0].as_number()))
            case 'floor':
                return NumberValue(math.floor(args[0].as_number()))


class SqrtFunction(Function):
    def execute(self, args: list[Value]) -> Value:
        if len(args) > 1:
            Error('The function takes only 1 argument.').call()
        return NumberValue(math.sqrt(args[0].as_number()))


class CosSinTanFunction(Function):
    def __init__(self, value: str):
        self.value = value

    def execute(self, args: list[Value]) -> Value:
        if len(args) > 1:
            Error('The function takes only 1 argument.').call()
        match self.value:
            case 'cos':
                return NumberValue(math.degrees(math.cos(args[0].as_number())))
            case 'sin':
                return NumberValue(math.degrees(math.sin(args[0].as_number())))
            case 'tan':
                return NumberValue(math.degrees(math.tan(args[0].as_number())))


class DegRadFunction(Function):
    def __init__(self, value: str):
        self.value = value

    def execute(self, args: list[Value]) -> Value:
        if len(args) > 1:
            Error('The function takes only 1 argument.').call()
        match self.value:
            case 'dtr':
                return NumberValue(math.radians(args[0].as_number()))
            case 'rtd':
                return NumberValue(math.degrees(args[0].as_number()))


class Math(Module):
    functions: dict[str, Function] = {
        'factorial': FactorialFunction(),
        'round': RoundFunction('round'),
        'roundUp': RoundFunction('roundUp'),
        'floor': RoundFunction('floor'),
        'sqrt': SqrtFunction(),
        'cos': CosSinTanFunction('cos'),
        'sin': CosSinTanFunction('sin'),
        'tan': CosSinTanFunction('tan'),
        'degToRad': DegRadFunction('dtr'),
        'radToDeg': DegRadFunction('rtd')
    }
    variables: dict[str, Value] = {
        'PI': NumberValue(math.pi),
        'E': NumberValue(math.e)
    }

    def init(self):
        for f in Math.functions:
            Functions.set(f, Math.functions[f])
        for f in Math.variables:
            Variables.set(f, Math.variables[f])
