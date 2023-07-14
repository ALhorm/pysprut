from Token import Token
from TokenType import TokenType


class Lexer:
    def __init__(self, code: str):
        self.code = code
        self.tokens: list[Token] = []
        self.pos: int = 0
        self.OPERATORS_CHARS: str = '+-*/(){}[]=><&|!.,:'
        self.OPERATORS: dict[str, TokenType] = {
            '+': TokenType.PLUS,
            '++': TokenType.PLUSPLUS,
            '-': TokenType.MINUS,
            '--': TokenType.MINUSMINUS,
            '*': TokenType.MULTIPLY,
            '/': TokenType.DIVIDE,
            '(': TokenType.OPEN_ROUND_BRACKET,
            ')': TokenType.CLOSE_ROUND_BRACKET,
            '{': TokenType.OPEN_CURLY_BRACKET,
            '}': TokenType.CLOSE_CURLY_BRACKET,
            '[': TokenType.OPEN_SQUARE_BRACKET,
            ']': TokenType.CLOSE_SQUARE_BRACKET,
            '=': TokenType.ASSIGN,
            ',': TokenType.COMMA,
            '.': TokenType.DOT,
            ':': TokenType.COLON,
            '==': TokenType.EQUALS,
            '>': TokenType.GREATER,
            '>=': TokenType.GREATER_ASSIGN,
            '<': TokenType.LESS,
            '<=': TokenType.LESS_ASSIGN,
            '!': TokenType.REJECT,
            '!=': TokenType.REJECT_ASSIGN,
            '&&': TokenType.AND,
            '||': TokenType.OR
        }
    
    def tokenize(self) -> list[Token]:
        while self.pos < len(self.code):
            current: str = self.peek(0)
            if current.isdigit():
                self.tokenize_number()
            elif current.isalpha():
                self.tokenize_word()
            elif current == '#':
                self.next()
                self.tokenize_hex_number()
            elif current == '"':
                self.tokenize_text()
            elif self.OPERATORS_CHARS.find(current) != -1:
                self.tokenize_operator()
            else:
                self.next()
        return self.tokens
    
    def tokenize_number(self):
        buffer: str = ''
        current: str = self.peek(0)
        while True:
            if current == '.':
                if buffer.find('.') != -1:
                    raise Exception('Invalid float number.')
            elif not current.isdigit():
                break
            buffer += current
            current = self.next()
        self.add_token(TokenType.NUMBER, buffer)
    
    def tokenize_hex_number(self):
        buffer: str = ''
        current: str = self.peek(0)
        while current.isdigit() or self.is_hex_number(current):
            buffer += current
            current = self.next()
        self.add_token(TokenType.HEX_NUMBER, buffer)

    @staticmethod
    def is_hex_number(current: str) -> bool:
        return 'abcdef'.find(current.lower()) != -1
    
    def tokenize_operator(self):
        current: str = self.peek(0)
        if current == '/':
            if self.peek(1) == '/':
                self.next()
                self.next()
                self.tokenize_comment()
                return
            elif self.peek(1) == '*':
                self.next()
                self.next()
                self.tokenize_multiline_comment()
                return
        buffer: str = ''
        while True:
            if buffer + current not in self.OPERATORS and buffer:
                self.add_token(self.OPERATORS[buffer])
                return
            buffer += current
            current = self.next()
    
    def tokenize_word(self):
        buffer: str = ''
        current: str = self.peek(0)
        while True:
            if not (current.isalpha() or current.isdigit()) and current != '_' and current != '$':
                break
            buffer += current
            current = self.next()

        match buffer:
            case 'print':
                self.add_token(TokenType.PRINT)
            case 'println':
                self.add_token(TokenType.PRINTLN)
            case 'if':
                self.add_token(TokenType.IF)
            case 'else':
                self.add_token(TokenType.ELSE)
            case 'while':
                self.add_token(TokenType.WHILE)
            case 'for':
                self.add_token(TokenType.FOR)
            case 'do':
                self.add_token(TokenType.DO)
            case 'break':
                self.add_token(TokenType.BREAK)
            case 'continue':
                self.add_token(TokenType.CONTINUE)
            case 'function':
                self.add_token(TokenType.FUNCTION)
            case 'return':
                self.add_token(TokenType.RETURN)
            case 'using':
                self.add_token(TokenType.USING)
            case _:
                self.add_token(TokenType.WORD, buffer)

    def tokenize_text(self):
        self.next()
        buffer: str = ''
        current: str = self.peek(0)
        while True:
            if current == '\\':
                current = self.next()
                match current:
                    case '"':
                        current = self.next()
                        buffer += '"'
                        continue
                    case 'n':
                        current = self.next()
                        buffer += '\n'
                        continue
                    case 't':
                        current = self.next()
                        buffer += '\t'
                        continue
                buffer += '\\'
                continue
            if current == '"':
                break
            buffer += current
            current = self.next()
        self.next()

        self.add_token(TokenType.TEXT, buffer)

    def tokenize_comment(self):
        current: str = self.peek(0)
        while '\r\n\0'.find(current) == -1:
            current = self.next()

    def tokenize_multiline_comment(self):
        current: str = self.peek(0)
        while True:
            if current == '\0':
                raise Exception('The multi-line comment was not closed.')
            if current == '*' and self.peek(1) == '/':
                break
            current = self.next()
        self.next()
        self.next()
    
    def next(self) -> str:
        self.pos += 1
        return self.peek(0)
    
    def peek(self, relative_position: int) -> str:
        position: int = self.pos + relative_position
        if position >= len(self.code):
            return '\0'
        return self.code[position]
    
    def add_token(self, token_type: TokenType, value: str | None = None):
        if value is not None:
            self.tokens.append(Token(token_type, value))
        else:
            self.tokens.append(Token(token_type, ''))
