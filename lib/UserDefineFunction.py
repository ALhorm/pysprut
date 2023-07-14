from .Value import Value
from .Function import Function
from .NumberValue import NumberValue
from AST import Statement
from AST.ReturnStatement import ReturnException


class UserDefineFunction(Function):
    def __init__(self, args_names: list[str], body: Statement):
        self.args_names = args_names
        self.body = body

    @property
    def args_amount(self) -> int:
        return len(self.args_names)

    def get_arg_name(self, index: int) -> str:
        if index < 0 or index > self.args_amount:
            return ''
        return self.args_names[index]

    def execute(self, args: list[Value]) -> Value:
        try:
            self.body.execute()
        except ReturnException as re:
            return re.value
        return NumberValue(0)
