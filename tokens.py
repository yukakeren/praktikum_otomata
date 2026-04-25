from dataclasses import dataclass

#  TOKEN DEFINITIONS
RESERVE_WORDS = {
    # Python
    'False', 'None', 'True', 'and', 'as', 'assert', 'async', 'await',
    'break', 'class', 'continue', 'def', 'del', 'elif', 'else', 'except',
    'finally', 'for', 'from', 'global', 'if', 'import', 'in', 'is',
    'lambda', 'nonlocal', 'not', 'or', 'pass', 'raise', 'return', 'try',
    'while', 'with', 'yield',
    # C
    'int', 'float', 'double', 'char', 'bool', 'void', 'string', 'var',
    'let', 'const', 'function', 'public', 'private', 'protected', 'static',
    'new', 'this', 'super', 'extends', 'implements', 'interface', 'enum',
    'switch', 'case', 'default', 'do', 'include', 'typedef', 'struct',
    'namespace', 'using', 'template', 'typename', 'auto', 'return',
    'print', 'input', 'range', 'len', 'type', 'list', 'dict', 'set', 'tuple',
}

MATH_FUNCTIONS = {
    'sin', 'cos', 'tan', 'log', 'log2', 'log10', 'sqrt', 'abs', 'pow',
    'exp', 'ceil', 'floor', 'round', 'max', 'min', 'sum', 'pi', 'e',
    'factorial', 'gcd', 'lcm', 'hypot', 'asin', 'acos', 'atan', 'atan2',
}

# Token categories
CATEGORY_RESERVE  = 'Reserve Word'
CATEGORY_SYMBOL   = 'Simbol / Tanda Baca'
CATEGORY_VARIABLE = 'Variabel'
CATEGORY_MATH     = 'Kalimat Matematika'
CATEGORY_NUMBER   = 'Angka'
CATEGORY_STRING   = 'String Literal'
CATEGORY_COMMENT  = 'Komentar'
CATEGORY_UNKNOWN  = 'Unknown'

# Color palette for categories
CATEGORY_COLORS = {
    CATEGORY_RESERVE:  '#FF6B6B',
    CATEGORY_SYMBOL:   '#FFD93D',
    CATEGORY_VARIABLE: '#6BCB77',
    CATEGORY_MATH:     '#4D96FF',
    CATEGORY_NUMBER:   '#C77DFF',
    CATEGORY_STRING:   '#F77F00',
    CATEGORY_COMMENT:  '#888888',
    CATEGORY_UNKNOWN:  '#CCCCCC',
}

CATEGORY_BG = {
    CATEGORY_RESERVE:  '#3D0000',
    CATEGORY_SYMBOL:   '#3D3000',
    CATEGORY_VARIABLE: '#003D10',
    CATEGORY_MATH:     '#001F3D',
    CATEGORY_NUMBER:   '#2D0050',
    CATEGORY_STRING:   '#3D1F00',
    CATEGORY_COMMENT:  '#1A1A1A',
    CATEGORY_UNKNOWN:  '#1A1A1A',
}


@dataclass
class Token:
    value: str
    category: str
    line: int
    col: int

    def to_dict(self):
        return {
            'token': self.value,
            'kategori': self.category,
            'baris': self.line,
            'kolom': self.col,
        }
