class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token = None
        self.index = -1
        self.advance()

    def advance(self):
        self.index += 1
        if self.index < len(self.tokens):
            self.current_token = self.tokens[self.index]
        else:
            self.current_token = None

    def match(self, token_type):
        if self.current_token is not None and self.current_token.type == token_type:
            self.advance()
            return True
        return False

    def stmt(self):
        if self.if_stmt() or self.block() or self.expr() or self.while_loop():
            return True
        return False

    def stmt_list(self):
        while self.stmt():
            if not self.match('SEMICOLON'):
                return False
        return True

    def if_stmt(self):
        if not self.match('IF'):
            return False
        if not self.match('LPAREN'):
            return False
        if not self.bool_expr():
            return False
        if not self.match('RPAREN'):
            return False
        if self.stmt():
            return True
        if not self.block():
            return False
        if self.match('ELSE'):
            if self.stmt():
                return True
            if not self.block():
                return False
        return True

    def block(self):
        if not self.match('LBRACE'):
            return False
        if not self.stmt_list():
            return False
        if not self.match('RBRACE'):
            return False
        return True

    def expr(self):
        if not self.term():
            return False
        while self.match('PLUS') or self.match('MINUS'):
            if not self.term():
                return False
        return True

    def term(self):
        if not self.fact():
            return False
        while self.match('TIMES') or self.match('DIVIDE') or self.match('MOD'):
            if not self.fact():
                return False
        return True

    def fact(self):
        if self.match('ID') or self.match('INT_LIT') or self.match('FLOAT_LIT'):
            return True
        if self.match('LPAREN'):
            if not self.expr():
                return False
            if not self.match('RPAREN'):
                return False
            return True
        return False

    def bool_expr(self):
        if not self.bterm():
            return False
        while self.match('GREATER') or self.match('LESS') or self.match('GREATER_EQUAL') or self.match('LESS_EQUAL'):
            if not self.bterm():
                return False
        return True

    def bterm(self):
        if not self.band():
            return False
        while self.match('EQUAL') or self.match('NOT_EQUAL'):
            if not self.band():
                return False
        return True

    def band(self):
        if not self.bor():
            return False
        while self.match('AND'):
            if not self.bor():
                return False
        return True

    def bor(self):
        if not self.expr():
            return False
        while self.match('OR'):
            if not self.expr():
                return False
        return True
