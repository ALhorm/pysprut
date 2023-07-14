from sys import exit


class Error:
    def __init__(self, message: str):
        self.message = message

    def call(self):
        print(f'\033[31mError: {self.message}\033[37m')
        exit(1)
