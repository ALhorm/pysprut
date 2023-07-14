from TokenType import TokenType


class Token:
    def __init__(self, token_type: TokenType, value: str):
        self.type = token_type
        self.value = value
    
    def __str__(self):
        return f'Token({self.type.name}, {self.value})'
