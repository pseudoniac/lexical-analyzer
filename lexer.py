from dataclasses import dataclass
import re

@dataclass
class Token:
	type: str
	value: str
	line: int
	column: int

TOKEN_SPECIFICATION = [
	('INTEGER',   r'\d+(\.\d+)?'),          # Integer or decimal number
    ('ASSIGN',   r'='),                     # Assignment operator
    ('SEMICOLON',      r';'),               # Statement terminator
    ('LPAREN',   r'\('),                    # Left parenthesis
    ('RPAREN',   r'\)'),                    # Right parenthesis
    ('LBRACE',   r'\{'),                    # Left BRACES
    ('RBRACE',   r'\}'),                    # Right BRACES
    ('IDENTIFIER',    r'[a-zA-Z_]\w*'),     # Identifiers / variable names
    ('ARITH_OP', r'\+|\-|\*|\/|\%'),         # Arithmetic operator
    ('REL_OP', r'==|!=|<|>|<=|>='),         # Relational operator
    ('NEWLINE',  r'\n'),           # Line break
    ('SKIP',     r'[ \t]+'),       # Skip spaces and tabs
    ('MISMATCH', r'.'),            # Any other character (error handling)
]

def tokenize(code: str):
    # Construct combined regex string
    tok_regex = '|'.join(f'(?P<{pair[0]}>{pair[1]})' for pair in TOKEN_SPECIFICATION)
    get_token = re.compile(tok_regex).match
    
    line_num = 1
    line_start = 0
    pos = 0
    
    match = get_token(code, pos)
    while match is not None:
        type_ = match.lastgroup
        value = match.group(type_)
        column = match.start() - line_start + 1
        
        if type_ == 'INTEGER':
            yield Token('INTEGER', value, line_num, column)
        elif type_ == 'IDENTIFIER':
            # Keywords can be checked here to separate them from identifiers
            keywords = {'if', 'else', 'while', 'let'}
            token_type = 'KEYWORD' if value in keywords else 'IDENTIFIER'
            yield Token(token_type, value, line_num, column)
        elif type_ in ('ASSIGN', 'SEMICOLON', 'ARITH_OP', 'LPAREN', 'RPAREN' ,'REL_OP' , 'LBRACE','RBRACE'):
            yield Token(type_, value, line_num, column)
        elif type_ == 'NEWLINE':
            line_start = match.end()
            line_num += 1
        elif type_ == 'SKIP':
            pass
        elif type_ == 'MISMATCH':
            raise SyntaxError(f"Unexpected character '{value}' at line {line_num}, column {column}")
        
        pos = match.end()
        match = get_token(code, pos)
        
"""    
this is for testing tokenize function pls remove comment sign to run this line
sample_code = \"""let x = 10 + 2.5;
if (x > 10) {
    x = x * 2;
}\"""

try:
    for token in tokenize(sample_code):
        print(token)
except SyntaxError as e:
    print(f"Lexer Error: {e}")

"""