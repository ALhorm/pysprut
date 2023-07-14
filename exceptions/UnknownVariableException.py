class UnknownVariableException(Exception):
    def __init__(self, variable: str):
        self.variable = variable

    def __str__(self):
        return f'Variable {self.variable} does not exist'
