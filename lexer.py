from tokens import KEYWORDS, OPERATORS, DELIMITERS, TOKEN_TYPE_MAP


class Token:
    def __init__(self, token_type, lexeme, line, column):
        self.token_type = token_type
        self.lexeme = lexeme
        self.line = line
        self.column = column

    def __repr__(self):
        return f"Token({self.token_type}, '{self.lexeme}', Ln:{self.line}, Col:{self.column})"


class SymbolTableEntry:
    def __init__(self, name, token_type, data_type, line, value=None):
        self.name = name
        self.token_type = token_type
        self.data_type = data_type
        self.line = line
        self.value = value

    def __repr__(self):
        return f"Symbol({self.name}, {self.data_type}, Ln:{self.line})"


class LexicalError:
    def __init__(self, message, line, column, severity="Error"):
        self.message = message
        self.line = line
        self.column = column
        self.severity = severity

    def __repr__(self):
        return f"[{self.severity}] Ln {self.line}, Col {self.column}: {self.message}"


class Lexer:
    def __init__(self):
        self.tokens = []
        self.symbol_table = {}
        self.errors = []
        self.source = ""
        self.pos = 0
        self.line = 1
        self.col = 1
        self.sym_id_counter = 1

    def reset(self, source):
        self.tokens = []
        self.symbol_table = {}
        self.errors = []
        self.source = source
        self.pos = 0
        self.line = 1
        self.col = 1
        self.sym_id_counter = 1

    def peek(self, offset=0):
        idx = self.pos + offset
        return self.source[idx] if idx < len(self.source) else '\0'

    def advance(self):
        ch = self.source[self.pos]
        self.pos += 1
        if ch == '\n':
            self.line += 1
            self.col = 1
        else:
            self.col += 1
        return ch

    def skip_whitespace(self):
        while self.pos < len(self.source) and self.peek() in ' \t\r\n':
            self.advance()

    def skip_single_line_comment(self):
        while self.pos < len(self.source) and self.peek() != '\n':
            self.advance()

    def skip_multi_line_comment(self):
        start_line, start_col = self.line, self.col
        while self.pos < len(self.source):
            if self.peek() == '*' and self.peek(1) == '/':
                self.advance()
                self.advance()
                return
            self.advance()
        self.errors.append(LexicalError(
            "Unterminated multi-line comment", start_line, start_col
        ))

    def read_string(self):
        start_line, start_col = self.line, self.col
        self.advance()
        value = ""
        while self.pos < len(self.source):
            ch = self.peek()
            if ch == '"':
                self.advance()
                return ('STRING_LITERAL', f'"{value}"', value)
            if ch == '\n':
                self.errors.append(LexicalError(
                    "Newline in string literal", self.line, self.col
                ))
                return ('STRING_LITERAL', f'"{value}"', value)
            if ch == '\\':
                self.advance()
                if self.pos < len(self.source):
                    value += '\\' + self.advance()
                continue
            value += self.advance()
        self.errors.append(LexicalError(
            "Unterminated string literal", start_line, start_col
        ))
        return ('STRING_LITERAL', f'"{value}"', value)

    def read_char(self):
        start_line, start_col = self.line, self.col
        self.advance()
        value = ""
        if self.pos < len(self.source):
            ch = self.peek()
            if ch == '\\':
                self.advance()
                if self.pos < len(self.source):
                    value = '\\' + self.advance()
            elif ch != "'":
                value = self.advance()
            if self.pos < len(self.source) and self.peek() == "'":
                self.advance()
                return ('CHAR_LITERAL', f"'{value}'", value)
        self.errors.append(LexicalError(
            "Invalid character literal", start_line, start_col
        ))
        return ('CHAR_LITERAL', f"'{value}'", value)

    def read_number(self):
        start_col = self.col
        num_str = ""
        is_float = False
        while self.pos < len(self.source) and self.peek().isdigit():
            num_str += self.advance()
        if self.peek() == '.':
            is_float = True
            num_str += self.advance()
            while self.pos < len(self.source) and self.peek().isdigit():
                num_str += self.advance()
            if num_str == '.':
                self.errors.append(LexicalError(
                    "Malformed number: lone decimal point",
                    self.line, start_col
                ))
                return ('FLOAT_CONSTANT', '.', '.')
            if self.peek() == '.':
                self.errors.append(LexicalError(
                    f"Malformed number: '{num_str}.' has multiple decimal points",
                    self.line, start_col
                ))
                num_str += self.advance()
                while self.pos < len(self.source) and self.peek().isdigit():
                    num_str += self.advance()
                return ('FLOAT_CONSTANT', num_str, num_str)
        if self.peek() in 'eE':
            is_float = True
            num_str += self.advance()
            if self.peek() in '+-':
                num_str += self.advance()
            while self.pos < len(self.source) and self.peek().isdigit():
                num_str += self.advance()
        if is_float:
            token_type = 'FLOAT_CONSTANT'
        else:
            token_type = 'INTEGER_CONSTANT'
        return (token_type, num_str, num_str)

    def read_identifier_or_keyword(self):
        start_col = self.col
        ident = ""
        while self.pos < len(self.source) and (self.peek().isalnum() or self.peek() == '_'):
            ident += self.advance()
        if ident in KEYWORDS:
            return ('KEYWORD', ident, ident)
        return ('IDENTIFIER', ident, ident)

    def read_operator_or_delimiter(self):
        ch = self.peek()
        if ch == '#':
            self.advance()
            return ('PREPROCESSOR', '#', '#')
        two_char = ch + self.peek(1) if self.pos + 1 < len(self.source) else ch
        if two_char in OPERATORS:
            self.advance()
            self.advance()
            return (OPERATORS[two_char], two_char, two_char)
        if ch in OPERATORS:
            self.advance()
            return (OPERATORS[ch], ch, ch)
        if ch in DELIMITERS:
            self.advance()
            return (DELIMITERS[ch], ch, ch)
        return None

    def tokenize(self):
        while self.pos < len(self.source):
            self.skip_whitespace()
            if self.pos >= len(self.source):
                break

            ch = self.peek()

            if ch == '/' and self.peek(1) == '/':
                self.skip_single_line_comment()
                continue
            if ch == '/' and self.peek(1) == '*':
                self.advance()
                self.advance()
                self.skip_multi_line_comment()
                continue

            if ch == '"':
                tok_type, lexeme, value = self.read_string()
                self.add_token(tok_type, lexeme)
                continue

            if ch == "'":
                tok_type, lexeme, value = self.read_char()
                self.add_token(tok_type, lexeme)
                continue

            if ch.isdigit():
                tok_type, lexeme, value = self.read_number()
                self.add_token(tok_type, lexeme)
                continue

            if ch.isalpha() or ch == '_':
                tok_type, lexeme, value = self.read_identifier_or_keyword()
                self.add_token(tok_type, lexeme)
                if tok_type == 'IDENTIFIER':
                    self.add_to_symbol_table(lexeme)
                continue

            result = self.read_operator_or_delimiter()
            if result:
                tok_type, lexeme, _ = result
                self.add_token(tok_type, lexeme)
                continue

            self.errors.append(LexicalError(
                f"Unexpected character: '{ch}' (ASCII: {ord(ch)})",
                self.line, self.col
            ))
            self.advance()

        self.add_token('EOF', '$')
        return self.tokens

    def add_token(self, token_type, lexeme):
        self.tokens.append(Token(token_type, lexeme, self.line, self.col))

    def add_to_symbol_table(self, name):
        if name not in self.symbol_table:
            data_type = self.infer_data_type(name)
            self.symbol_table[name] = SymbolTableEntry(
                name=name,
                token_type='IDENTIFIER',
                data_type=data_type,
                line=self.line,
                value=None
            )

    def infer_data_type(self, name):
        for i in range(len(self.tokens) - 1, -1, -1):
            tok = self.tokens[i]
            if tok.token_type == 'KEYWORD' and tok.lexeme in {
                'int', 'float', 'char', 'double', 'void', 'long',
                'short', 'unsigned', 'signed', 'struct', 'const'
            }:
                return tok.lexeme
        for tok in self.tokens:
            if tok.token_type == 'KEYWORD' and tok.lexeme in {
                'int', 'float', 'char', 'double', 'void', 'long',
                'short', 'unsigned', 'signed', 'struct', 'const'
            }:
                idx = self.tokens.index(tok)
                for j in range(idx + 1, min(idx + 3, len(self.tokens))):
                    if j < len(self.tokens) and self.tokens[j].lexeme == name:
                        return tok.lexeme
        return 'unknown'

    def get_summary(self):
        token_count = len(self.tokens) - 1
        error_count = len(self.errors)
        symbol_count = len(self.symbol_table)
        return {
            'token_count': token_count,
            'error_count': error_count,
            'symbol_count': symbol_count,
            'has_errors': error_count > 0
        }
