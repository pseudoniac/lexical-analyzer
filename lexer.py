from dataclasses import dataclass
from collections import Counter # Library for count frequency of element so why not use it :)
import re

@dataclass
class Token:
    type: str
    value: str
    line: int
    column: int

TOKEN_SPECIFICATION = [
	('INTEGER',   r'\d+(\.\d+)?'),          # Integer or decimal number
    ('REL_OP', r'==|!=|<=|>=|<|>'),         # Relational operator
    ('COMMENTLINE', r'(#|//).*'), # Comment line
    ('ASSIGN',   r'='),                     # Assignment operator
    ('SEMICOLON',      r';'),               # Statement terminator
    ('LPAREN',   r'\('),                    # Left parenthesis
    ('RPAREN',   r'\)'),                    # Right parenthesis
    ('LBRACE',   r'\{'),                    # Left BRACES
    ('RBRACE',   r'\}'),                    # Right BRACES
    ('IDENTIFIER',    r'[a-zA-Z_]\w*'),     # Identifiers / variable names
    ('ARITH_OP', r'\+|\-|\*|\/|\%'),         # Arithmetic operator
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
            keywords = {'if', 'else', 'while', 'let', 'print'}
            token_type = 'KEYWORD' if value in keywords else 'IDENTIFIER'
            yield Token(token_type, value, line_num, column)
        elif type_ in ('ASSIGN', 'SEMICOLON', 'ARITH_OP', 'LPAREN', 'RPAREN' ,'REL_OP' , 'LBRACE','RBRACE'):
            yield Token(type_, value, line_num, column)
        elif type_ == 'NEWLINE':
            line_start = match.end()
            line_num += 1
        elif type_ in ('SKIP','COMMENTLINE'):
            pass
        elif type_ == 'MISMATCH':
            raise SyntaxError(f"Unexpected character '{value}' at line {line_num}, column {column}")
        
        pos = match.end()
        match = get_token(code, pos)

def analyze_tokens(code: str):
    tokens = list(tokenize(code))
    
    total_count = len(tokens)
    type_counts = Counter(t.type for t in tokens)
    
    return total_count, type_counts

#replace here if want to test other code
sample_code = """  # Public test 2: while loops with a nested if
# Prints the factorial of 5, then counts the multiples of 3 from 1 to 12
let n = 5;
let fact = 1;
while (n > 1) {
    fact = fact * n;
    n = n - 1;
}
print(fact);

let i = 1;
let count = 0;
while (i <= 12) {
    if (i % 3 == 0) {
        count = count + 1;
    }
    i = i + 1;
}
print(count);"""    

try:
    print("== TOKEN STREAM ==")
    print(f"{'LINE':>4}  {'COL':>4}  {'TYPE':<12} {'LEXEME'}")
    tokens = list(tokenize(sample_code))
    for token in tokens:
        print(f"{token.line:>4}  {token.column:>4}  {token.type:<12} {token.value}")
        
    total, breakdown = analyze_tokens(sample_code)

    print("\n== TOKEN COUNTS ==")
    print(f"Total Tokens: {total}")
    for token_type, count in breakdown.items():
        print(f"  {token_type}: {count}")

except SyntaxError as e:
    print(f"Lexer Error: {e}")
