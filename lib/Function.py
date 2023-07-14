from .Value import Value


class Function:
    def execute(self, args: list[Value]) -> Value:
        raise NotImplementedError
