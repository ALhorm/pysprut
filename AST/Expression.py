from lib import Value


class Expression:
    def eval(self) -> Value:
        raise NotImplementedError
