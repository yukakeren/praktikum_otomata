import re
from typing import List, Tuple

from tokens import (
    Token, RESERVE_WORDS, MATH_FUNCTIONS,
    CATEGORY_COMMENT, CATEGORY_STRING, CATEGORY_NUMBER,
    CATEGORY_RESERVE, CATEGORY_MATH, CATEGORY_SYMBOL,
    CATEGORY_VARIABLE, CATEGORY_UNKNOWN
)


class Lexer:
    # Regex patterns ordered by priority
    TOKEN_PATTERNS: List[Tuple[str, str]] = [
        ('COMMENT_SINGLE', r'//[^\n]*|#[^\n]*'),
        ('COMMENT_MULTI',  r'/\*[\s\S]*?\*/'),
        ('STRING_DQ3',     r'"""[\s\S]*?"""'),
        ('STRING_SQ3',     r"'''[\s\S]*?'''"),
        ('STRING_DQ',      r'"(?:\\.|[^"\\])*"'),
        ('STRING_SQ',      r"'(?:\\.|[^'\\])*'"),
        ('FLOAT',          r'\b\d+\.\d*(?:[eE][+-]?\d+)?\b|\b\d*\.\d+(?:[eE][+-]?\d+)?\b'),
        ('INTEGER',        r'\b\d+\b'),
        ('MATH_EXPR',      r'(?:[a-zA-Z_]\w*\s*=\s*)?(?:[a-zA-Z_]\w*\s*(?:[+\-*/%^]|\*\*)\s*)+[a-zA-Z0-9_\.\(\)]+'),
        ('IDENTIFIER',     r'[a-zA-Z_]\w*'),
        ('OPERATOR',       r'\*\*|//|<<|>>|<=|>=|==|!=|[+\-*/%=<>&|^~!]'),
        ('DELIMITER',      r'[(){}\[\],;:.]'),
        ('WHITESPACE',     r'\s+'),
        ('UNKNOWN',        r'.'),
    ]

    def __init__(self):
        parts = '|'.join(f'(?P<{name}>{pat})' for name, pat in self.TOKEN_PATTERNS)
        self._regex = re.compile(parts)

    def _is_math_expression(self, text: str) -> bool:
        has_op = bool(re.search(r'[\+\-\*/\^%]|\*\*', text))
        has_num_or_id = bool(re.search(r'[a-zA-Z0-9_]', text))
        return has_op and has_num_or_id

    def _categorize(self, kind: str, value: str) -> str:
        if kind in ('COMMENT_SINGLE', 'COMMENT_MULTI'):
            return CATEGORY_COMMENT
        if kind in ('STRING_DQ3', 'STRING_SQ3', 'STRING_DQ', 'STRING_SQ'):
            return CATEGORY_STRING
        if kind in ('FLOAT', 'INTEGER'):
            return CATEGORY_NUMBER
        if kind == 'IDENTIFIER':
            if value in RESERVE_WORDS:
                return CATEGORY_RESERVE
            if value in MATH_FUNCTIONS:
                return CATEGORY_MATH
            return CATEGORY_VARIABLE
        if kind in ('OPERATOR', 'DELIMITER'):
            return CATEGORY_SYMBOL
        if kind == 'MATH_EXPR':
            return CATEGORY_MATH
        return CATEGORY_UNKNOWN

    def tokenize(self, source: str) -> List[Token]:
        tokens: List[Token] = []
        line, line_start = 1, 0

        for m in self._regex.finditer(source):
            kind = m.lastgroup
            value = m.group()

            if kind == 'WHITESPACE':
                for ch in value:
                    if ch == '\n':
                        line += 1
                        line_start = m.start() + value.index('\n', 0) + 1
                continue

            col = m.start() - line_start + 1
            category = self._categorize(kind, value)
            tokens.append(Token(value, category, line, col))

            # update line counter for multi-line tokens
            newlines = value.count('\n')
            if newlines:
                line += newlines
                line_start = m.start() + value.rfind('\n') + 1

        return tokens
