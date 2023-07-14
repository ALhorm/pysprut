from lib import Value, Functions, Function, UserDefineFunction, Variables, FunctionValue
from exceptions import UnknownVariableException
from .Expression import Expression


class FunctionalExpression(Expression):
    def __init__(self, name: str | Expression, arguments: list[Expression] | None = None):
        self.name = name
        if arguments is not None:
            self.arguments = arguments
        else:
            self.arguments = []

    def __str__(self):
        return f'{self.name}({str(self.arguments)})'

    def add_argument(self, argument: Expression):
        self.arguments.append(argument)

    def consume_function(self, expr: Expression):
        try:
            value: Value = expr.eval()
            if isinstance(value, FunctionValue):
                return value.value
            return self.get_function(value.as_string())
        except UnknownVariableException as ex:
            return self.get_function(ex.variable)

    @staticmethod
    def get_function(key: str) -> Function:
        if Functions.is_exists(key):
            return Functions.get(key)
        if Variables.is_exists(key):
            variable: Value = Variables.get(key)
            if isinstance(variable, FunctionValue):
                return variable.value
        raise Exception(f'Unknown function {key}.')

    def eval(self) -> Value:
        values: list[Value] = []
        for i, v in enumerate(self.arguments):
            values.append(self.arguments[i].eval())

        function: Function = self.consume_function(self.name)
        if isinstance(function, UserDefineFunction):
            user_function: UserDefineFunction = function
            if len(self.arguments) != user_function.args_amount:
                raise Exception('Args amount mismatch.')

            Variables.push()
            for i, v in enumerate(self.arguments):
                Variables.set(user_function.get_arg_name(i), values[i])
            result: Value = user_function.execute(values)
            Variables.pop()
            return result

        return function.execute(values)
