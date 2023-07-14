from Token import Token
from TokenType import TokenType
from AST import *
from lib import UserDefineFunction
from exceptions import Error


class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.pos: int = 0
        self.EOF: Token = Token(TokenType.EOF, '')
    
    def parse(self) -> Statement:
        result: BlockStatement = BlockStatement()
        while not self.match(TokenType.EOF):
            result.add(self.statement())
        return result

    def block(self) -> Statement:
        block: BlockStatement = BlockStatement()
        self.consume(TokenType.OPEN_CURLY_BRACKET)
        while not self.match(TokenType.CLOSE_CURLY_BRACKET):
            block.add(self.statement())
        return block

    def statement_or_block(self) -> Statement:
        if self.get(0).type == TokenType.OPEN_CURLY_BRACKET:
            return self.block()
        return self.statement()

    def statement(self) -> Statement | Expression:
        if self.match(TokenType.PRINT):
            return PrintStatement(self.expression())
        if self.match(TokenType.PRINTLN):
            return PrintStatement(self.expression(), new_line=True)
        if self.match(TokenType.IF):
            return self.if_else()
        if self.match(TokenType.WHILE):
            return self.while_statement()
        if self.match(TokenType.FOR):
            return self.for_statement()
        if self.match(TokenType.DO):
            return self.do_while_statement()
        if self.match(TokenType.BREAK):
            return BreakStatement()
        if self.match(TokenType.CONTINUE):
            return ContinueStatement()
        if self.match(TokenType.FUNCTION):
            return self.function_define()
        if self.match(TokenType.RETURN):
            return ReturnStatement(self.expression())
        if self.match(TokenType.USING):
            return self.using_statement()
        if self.look_match(0, TokenType.WORD) and self.look_match(1, TokenType.OPEN_ROUND_BRACKET):
            return FunctionStatement(self.function(self.qualified_name()))
        if self.look_match(0, TokenType.WORD) and self.look_match(1, TokenType.DOT):
            function: Expression = self.object()
            return FunctionStatement(self.function(function))
        return self.assignment_statement()

    def assignment_statement(self) -> Statement:
        if self.look_match(0, TokenType.WORD) and self.look_match(1, TokenType.ASSIGN):
            variable: str = self.consume(TokenType.WORD).value
            self.consume(TokenType.ASSIGN)
            return AssignmentStatement(variable, self.expression())
        if self.look_match(0, TokenType.WORD) and (self.look_match(1, TokenType.PLUSPLUS) or self.look_match(1, TokenType.MINUSMINUS)):
            variable: str = self.consume(TokenType.WORD).value
            operation: str = ''
            if self.match(TokenType.PLUSPLUS):
                operation = '++'
            elif self.match(TokenType.MINUSMINUS):
                operation = '--'
            return UnaryStatement(variable, operation)
        if self.look_match(0, TokenType.WORD) and self.look_match(1, TokenType.COLON):
            variable: str = self.consume(TokenType.WORD).value
            self.consume(TokenType.COLON)
            variable_type: str = self.consume(TokenType.WORD).value
            self.consume(TokenType.ASSIGN)
            return AssignmentStatement(variable, self.expression(), variable_type=variable_type)
        if self.look_match(0, TokenType.WORD) and self.look_match(1, TokenType.OPEN_SQUARE_BRACKET):
            array: AccessExpression = self.element()
            self.consume(TokenType.ASSIGN)
            return ArrayAssignmentStatement(array, self.expression())
        Error(f'Unknown statement {self.get(0)}.').call()

    def if_else(self):
        self.consume(TokenType.OPEN_ROUND_BRACKET)
        condition: Expression = self.expression()
        self.consume(TokenType.CLOSE_ROUND_BRACKET)
        if_statement: Statement = self.statement_or_block()
        else_statement: Statement | None = None
        if self.match(TokenType.ELSE):
            else_statement = self.statement_or_block()
        return IfStatement(condition, if_statement, else_statement)

    def while_statement(self) -> Statement:
        self.consume(TokenType.OPEN_ROUND_BRACKET)
        condition: Expression = self.expression()
        self.consume(TokenType.CLOSE_ROUND_BRACKET)
        statement: Statement = self.statement_or_block()
        return WhileStatement(condition, statement)

    def do_while_statement(self) -> Statement:
        statement: Statement = self.statement_or_block()
        self.consume(TokenType.WHILE)
        self.consume(TokenType.OPEN_ROUND_BRACKET)
        condition: Expression = self.expression()
        self.consume(TokenType.CLOSE_ROUND_BRACKET)
        return DoWhileStatement(condition, statement)

    def for_statement(self) -> Statement:
        self.consume(TokenType.OPEN_ROUND_BRACKET)
        initialization: Statement = self.assignment_statement()
        self.consume(TokenType.COMMA)
        condition: Expression = self.expression()
        self.consume(TokenType.COMMA)
        action: Statement = self.assignment_statement()
        self.consume(TokenType.CLOSE_ROUND_BRACKET)
        statement: Statement = self.statement_or_block()
        return ForStatement(initialization, condition, action, statement)

    def using_statement(self) -> Statement:
        module_values: dict[str, str] = {}
        if self.match(TokenType.OPEN_ROUND_BRACKET):
            while not self.match(TokenType.CLOSE_ROUND_BRACKET):
                if self.look_match(1, TokenType.COLON):
                    function = self.consume(TokenType.WORD).value
                    self.consume(TokenType.COLON)
                    module_values[function] = self.consume(TokenType.WORD).value
                    self.match(TokenType.COMMA)
                else:
                    module_values[self.consume(TokenType.WORD).value] = ''
                    self.match(TokenType.COMMA)
        return UsingStatement(self.expression(), module_values)

    def function_define(self) -> FunctionDefineStatement:
        name: str = self.consume(TokenType.WORD).value
        self.consume(TokenType.OPEN_ROUND_BRACKET)
        args_names: list[str] = []
        while not self.match(TokenType.CLOSE_ROUND_BRACKET):
            args_names.append(self.consume(TokenType.WORD).value)
            self.match(TokenType.COMMA)
        body: Statement = self.statement_or_block()
        return FunctionDefineStatement(name, args_names, body)

    def function(self, qualified_name_expr: Expression) -> FunctionalExpression:
        self.consume(TokenType.OPEN_ROUND_BRACKET)
        function: FunctionalExpression = FunctionalExpression(qualified_name_expr)
        while not self.match(TokenType.CLOSE_ROUND_BRACKET):
            function.add_argument(self.expression())
            self.match(TokenType.COMMA)
        return function

    def array(self) -> ArrayExpression:
        self.consume(TokenType.OPEN_SQUARE_BRACKET)
        elements: list[Expression] = []
        while not self.match(TokenType.CLOSE_SQUARE_BRACKET):
            elements.append(self.expression())
            self.match(TokenType.COMMA)
        return ArrayExpression(elements)

    def dictionary(self) -> DictionaryExpression:
        self.consume(TokenType.OPEN_CURLY_BRACKET)
        elements: dict[Expression, Expression] = {}
        while not self.match(TokenType.CLOSE_CURLY_BRACKET):
            key: Expression = self.primary()
            self.consume(TokenType.COLON)
            value: Expression = self.expression()
            elements[key] = value
            self.match(TokenType.COMMA)
        return DictionaryExpression(elements)

    def element(self) -> AccessExpression:
        variable: str = self.consume(TokenType.WORD).value
        indices: list[Expression] = []
        while True:
            self.consume(TokenType.OPEN_SQUARE_BRACKET)
            indices.append(self.expression())
            self.consume(TokenType.CLOSE_SQUARE_BRACKET)
            if not self.look_match(0, TokenType.OPEN_SQUARE_BRACKET):
                break
        return AccessExpression(variable, indices)

    def object(self) -> AccessExpression:
        variable: str = self.consume(TokenType.WORD).value
        indices: list[Expression] = []
        while self.match(TokenType.DOT):
            field_name: str = self.consume(TokenType.WORD).value
            indices.append(ValueExpression(field_name))
        return AccessExpression(variable, indices)

    def expression(self) -> Expression:
        return self.logical_or()

    def logical_or(self) -> Expression:
        result: Expression = self.logical_and()

        while True:
            if self.match(TokenType.OR):
                result = ConditionalExpression(Operator.OR, result, self.logical_and())
                continue
            break

        return result

    def logical_and(self) -> Expression:
        result: Expression = self.equality()

        while True:
            if self.match(TokenType.AND):
                result = ConditionalExpression(Operator.AND, result, self.equality())
                continue
            break

        return result

    def equality(self) -> Expression:
        result: Expression = self.conditional()

        if self.match(TokenType.EQUALS):
            return ConditionalExpression(Operator.EQUALS, result, self.conditional())
        if self.match(TokenType.REJECT_ASSIGN):
            return ConditionalExpression(Operator.REJECT_ASSIGN, result, self.conditional())

        return result

    def conditional(self) -> Expression:
        result: Expression = self.additive()

        while True:
            if self.match(TokenType.GREATER):
                result = ConditionalExpression(Operator.GREATER, result, self.additive())
                continue
            if self.match(TokenType.GREATER_ASSIGN):
                result = ConditionalExpression(Operator.GREATER_ASSIGN, result, self.additive())
                continue
            if self.match(TokenType.LESS):
                result = ConditionalExpression(Operator.LESS, result, self.additive())
                continue
            if self.match(TokenType.LESS_ASSIGN):
                result = ConditionalExpression(Operator.LESS_ASSIGN, result, self.additive())
                continue
            break

        return result
    
    def additive(self) -> Expression:
        result: Expression = self.multiplicative()
        
        while True:
            if self.match(TokenType.PLUS):
                result = BinaryExpression('+', result, self.multiplicative())
                continue
            if self.match(TokenType.MINUS):
                result = BinaryExpression('-', result, self.multiplicative())
                continue
            break

        return result
    
    def multiplicative(self) -> Expression:
        result: Expression = self.unary()
        
        while True:
            if self.match(TokenType.MULTIPLY):
                result = BinaryExpression('*', result, self.unary())
                continue
            if self.match(TokenType.DIVIDE):
                result = BinaryExpression('/', result, self.unary())
                continue
            break
        
        return result
    
    def unary(self) -> Expression:
        if self.match(TokenType.PLUSPLUS):
            return UnaryExpression('++', self.primary(), variable=self.get(0).value)
        if self.match(TokenType.MINUSMINUS):
            return UnaryExpression('--', self.primary(), variable=self.get(0).value)
        if self.match(TokenType.PLUS):
            return self.primary()
        if self.match(TokenType.MINUS):
            return UnaryExpression('-', self.primary())
        return self.primary()
    
    def primary(self) -> Expression:
        if self.match(TokenType.FUNCTION):
            self.consume(TokenType.OPEN_ROUND_BRACKET)
            arg_names: list[str] = []
            while not self.match(TokenType.CLOSE_ROUND_BRACKET):
                arg_names.append(self.consume(TokenType.WORD).value)
                self.match(TokenType.COMMA)
            body: Statement = self.statement_or_block()
            return ValueExpression(UserDefineFunction(arg_names, body))
        if self.match(TokenType.OPEN_ROUND_BRACKET):
            result: Expression = self.expression()
            self.match(TokenType.CLOSE_ROUND_BRACKET)
            return result
        return self.variable()

    def variable(self) -> Expression:
        if self.look_match(0, TokenType.WORD) and self.look_match(1, TokenType.OPEN_ROUND_BRACKET):
            return self.function(ValueExpression(self.consume(TokenType.WORD).value))
        qualified_name_expr: Expression = self.qualified_name()
        if qualified_name_expr is not None:
            if self.look_match(0, TokenType.OPEN_ROUND_BRACKET):
                return self.function(qualified_name_expr)
            return qualified_name_expr
        if self.look_match(0, TokenType.OPEN_SQUARE_BRACKET):
            return self.array()
        if self.look_match(0, TokenType.OPEN_CURLY_BRACKET):
            return self.dictionary()
        return self.value()

    def qualified_name(self) -> Expression | None:
        current: Token = self.get(0)
        if self.look_match(0, TokenType.WORD) and self.look_match(1, TokenType.OPEN_SQUARE_BRACKET):
            return self.element()
        if self.look_match(0, TokenType.WORD) and self.look_match(1, TokenType.DOT):
            return self.object()
        if self.match(TokenType.WORD):
            return VariableExpression(current.value)
        return None

    def value(self):
        current: Token = self.get(0)
        if self.match(TokenType.NUMBER):
            return ValueExpression(float(current.value))
        if self.match(TokenType.HEX_NUMBER):
            return ValueExpression(float(int(current.value, 16)))
        if self.match(TokenType.TEXT):
            return ValueExpression(current.value)
        Error(f'Unknown expression {current}.').call()

    def match(self, token_type: TokenType) -> bool:
        current: Token = self.get(0)
        if token_type != current.type:
            return False
        self.pos += 1
        return True

    def look_match(self, position: int, token_type: TokenType):
        return self.get(position).type == token_type

    def consume(self, token_type: TokenType) -> Token:
        current: Token = self.get(0)
        if token_type != current.type:
            Error(f'A {token_type.name} was expected, but a {current.type.name} was received.').call()
        self.pos += 1
        return current
    
    def get(self, relative_position: int) -> Token:
        position: int = self.pos + relative_position
        if position >= len(self.tokens):
            return self.EOF
        return self.tokens[position]
