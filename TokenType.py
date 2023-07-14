from enum import Enum


class TokenType(Enum):
    NUMBER = r'\d+'
    HEX_NUMBER = r'#\d+'
    WORD = r'\w+'
    TEXT = r'\".*\"'

    PRINT = r'print'
    PRINTLN = r'println'
    IF = r'if'
    ELSE = r'else'
    WHILE = r'while'
    FOR = r'for'
    DO = r'do'
    BREAK = r'break'
    CONTINUE = r'continue'
    FUNCTION = r'function'
    RETURN = r'return'
    USING = r'using'
    
    PLUS = r'\+'
    PLUSPLUS = r'\+\+'
    MINUS = r'\-'
    MINUSMINUS = r'\-\-'
    MULTIPLY = r'\*'
    DIVIDE = r'/'

    EQUALS = r'=='
    GREATER = r'>'
    GREATER_ASSIGN = r'>='
    LESS = r'<'
    LESS_ASSIGN = r'<='
    REJECT = r'!'
    REJECT_ASSIGN = r'!='
    AND = r'&&'
    OR = r'||'
    
    OPEN_ROUND_BRACKET = r'\('
    CLOSE_ROUND_BRACKET = r'\)'
    OPEN_CURLY_BRACKET = r'{'
    CLOSE_CURLY_BRACKET = r'}'
    OPEN_SQUARE_BRACKET = r'\['
    CLOSE_SQUARE_BRACKET = r'\]'
    ASSIGN = r'='
    COMMA = r','
    COLON = r':'
    DOT = r'\.'
    
    EOF = None
