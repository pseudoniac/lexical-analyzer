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
    ('COMMENTLINE', r'(#|//).*'), # Comment line
    ('SKIP', r'[ \t]+'),       # Skip spaces and tabs
    ('NEWLINE', r'\n'),           # Line break
    ('INVALID_IDENT', r'(\d+[a-zA-Z0-9_@$#~`?!\\-]*[a-zA-Z_@$#~`?!\\-][a-zA-Z0-9_@$#~`?!\\-]*|[a-zA-Z_]\w*[@$#~`?!\\][a-zA-Z0-9_@$#~`?!\\-]*)'), # Identifier containing/ending with illegal symbols (e.g., a2@, var#name)
	('INTEGER', r'\d+(\.\d+)?'),          # Integer or decimal number
    ('IDENTIFIER', r'[a-zA-Z_]\w*'),     # Identifiers / variable names
    ('REL_OP', r'==|!=|<=|>=|<|>'),         # Relational operator
    ('ASSIGN', r'='),                     # Assignment operator
    ('ARITH_OP', r'\+|\-|\*|\/|\%'),         # Arithmetic operator
    ('SEMICOLON', r';'),               # Statement terminator
    ('LPAREN', r'\('),                    # Left parenthesis
    ('RPAREN', r'\)'),                    # Right parenthesis
    ('LBRACE', r'\{'),                    # Left BRACES
    ('RBRACE', r'\}'),                    # Right BRACES
    ('MISMATCH', r'.'),            # Any other character (error handling)
]

FREQUENCY_BREAKDOWN_ORDER = [
        'KEYWORD',
        'IDENTIFIER',
        'INTEGER',
        'ARITH_OP',
        'REL_OP',
        'ASSIGN',
        'LPAREN',
        'RPAREN',
        'LBRACE',
        'RBRACE',
        'SEMICOLON',
    ]

def tokenize(code: str):
    # Construct combined regex string
    tok_regex = '|'.join(f'(?P<{pair[0]}>{pair[1]})' for pair in TOKEN_SPECIFICATION)
    get_token = re.compile(tok_regex).match
    
    line_num = 1
    line_start = 0
    pos = 0

    tokens = []
    errors = []

    match = get_token(code, pos)
    while match is not None:
        type_ = match.lastgroup
        value = match.group(type_)
        column = match.start() - line_start + 1

        if type_ == 'INVALID_IDENT':
            errors.append(f"at line {line_num}, col {column}: malformed token '{value}'")
        elif type_ == 'MISMATCH':
            errors.append(f"at line {line_num}, col {column}: invalid character '{value}'")
        elif type_ in ('SKIP','COMMENTLINE'):
            pass
        elif type_ == 'NEWLINE':
            line_start = match.end()
            line_num += 1
        else:
            if type_ == 'INTEGER':
                tokens.append(Token('INTEGER', value, line_num, column))
            elif type_ == 'IDENTIFIER':
                # Keywords can be checked here to separate them from identifiers
                keywords = {'if', 'else', 'while', 'let', 'print'}
                token_type = 'KEYWORD' if value in keywords else 'IDENTIFIER'
                tokens.append(Token(token_type, value, line_num, column))
            elif type_ in ('ASSIGN', 'SEMICOLON', 'ARITH_OP', 'LPAREN', 'RPAREN' ,'REL_OP' , 'LBRACE','RBRACE'):
                tokens.append(Token(type_, value, line_num, column))
        
        pos = match.end()
        match = get_token(code, pos)

    return tokens, errors

def print_token(tokens, errors):
    print("== TOKEN STREAM ==")
    print(f"{'LINE':>4} {'COL':>4}  {'TYPE':<11} {'LEXEME'}")
    for t in tokens:
        print(f"{t.line:>4} {t.column:>4}  {t.type:<11} {t.value}")

    if errors:
        for err in errors:
            print(f"LexicalError {err}")
            
        
    total = len(tokens)
    breakdown = Counter(t.type for t in tokens)

    category_map = {
            'KEYWORD':    breakdown['KEYWORD'],
            'IDENTIFIER': breakdown['IDENTIFIER'],
            'INTEGER':    breakdown['INTEGER'],
            'ARITH_OP':   breakdown['ARITH_OP'],
            'REL_OP':     breakdown['REL_OP'],
            'ASSIGN':     breakdown['ASSIGN'],
            'LPAREN':     breakdown['LPAREN'],
            'RPAREN':     breakdown['RPAREN'],
            'LBRACE':     breakdown['LBRACE'],
            'RBRACE':     breakdown['RBRACE'],
            'SEMICOLON':  breakdown['SEMICOLON'],
        }

    print("\n== TOKEN COUNTS ==")
    print(f"Total tokens: {total}")
    for category in FREQUENCY_BREAKDOWN_ORDER:
        count = category_map[category]
        if count > 0:
            print(f"  {category:<11} {count}")


def main():
   #replace here if want to test other code
    sample_code = """# Public test 4: two lexical errors, both must be reported
    let price = 250;
    let rate = 6;
    let tax = price $ rate / 100;
    let 2nd = tax + 1;
    print(tax);
    """   
    tokens, errors = tokenize(sample_code)

    print_token(tokens, errors)

    if errors:
        print(f"\n{len(errors)} lexical error(s). Parsing skipped.")
        #stop here - skip parser call 
        return

main()