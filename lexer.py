from dataclasses import dataclass
import re

@dataclass
class Token:
	type: str
	value: str
	line: int
	column: int

Token_Specification = [
	('NUMBER',   r'\d+(\.\d+)?'),  # Integer or decimal number
    ('ASSIGN',   r'='),            # Assignment operator
    ('END',      r';'),            # Statement terminator
    ('PLUS',     r'\+'),           # Addition
    ('MINUS',    r'-'),            # Subtraction
    ('TIMES',    r'\*'),           # Multiplication
    ('DIVIDE',   r'/'),            # Division
    ('LPAREN',   r'\('),           # Left parenthesis
    ('RPAREN',   r'\)'),           # Right parenthesis
    ('IDENT',    r'[a-zA-Z_]\w*'), # Identifiers / variable names
    ('NEWLINE',  r'\n'),           # Line break
    ('SKIP',     r'[ \t]+'),       # Skip spaces and tabs
    ('MISMATCH', r'.'),            # Any other character (error handling)
]