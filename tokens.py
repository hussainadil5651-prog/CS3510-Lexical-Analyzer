KEYWORDS = {
    'auto', 'break', 'case', 'char', 'const', 'continue', 'default', 'do',
    'double', 'else', 'enum', 'extern', 'float', 'for', 'goto', 'if',
    'int', 'long', 'register', 'return', 'short', 'signed', 'sizeof',
    'static', 'struct', 'switch', 'typedef', 'union', 'unsigned', 'void',
    'volatile', 'while', 'include', 'define'
}

OPERATORS = {
    '+': 'PLUS', '-': 'MINUS', '*': 'MULTIPLY', '/': 'DIVIDE',
    '%': 'MODULO', '=': 'ASSIGN', '==': 'EQUAL', '!=': 'NOT_EQUAL',
    '<': 'LESS_THAN', '>': 'GREATER_THAN', '<=': 'LESS_EQUAL',
    '>=': 'GREATER_EQUAL', '&&': 'LOGICAL_AND', '||': 'LOGICAL_OR',
    '!': 'LOGICAL_NOT', '++': 'INCREMENT', '--': 'DECREMENT',
    '&': 'BITWISE_AND', '|': 'BITWISE_OR', '^': 'BITWISE_XOR',
    '~': 'BITWISE_NOT', '<<': 'LEFT_SHIFT', '>>': 'RIGHT_SHIFT',
    '+=': 'ADD_ASSIGN', '-=': 'SUB_ASSIGN', '*=': 'MUL_ASSIGN',
    '/=': 'DIV_ASSIGN', '%=': 'MOD_ASSIGN', '->': 'ARROW'
}

DELIMITERS = {
    '(': 'LPAREN', ')': 'RPAREN', '{': 'LBRACE', '}': 'RBRACE',
    '[': 'LBRACKET', ']': 'RBRACKET', ';': 'SEMICOLON', ',': 'COMMA',
    '.': 'DOT', ':': 'COLON', '?': 'QUESTION', '#': 'HASH'
}

TOKEN_TYPE_MAP = {}
for op, name in OPERATORS.items():
    TOKEN_TYPE_MAP[op] = name
for delim, name in DELIMITERS.items():
    TOKEN_TYPE_MAP[delim] = name
