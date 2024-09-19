import ply.lex as lex

# トークンリスト
tokens = (
    'EXTERN', 'CRATE', 'FN', 'LET', 'MUT', 'IF', 'ELSE', 'WHILE', 'FOR', 'IN', 'MATCH', 'STRUCT', 'ENUM', 'IMPL', 'USE', 'MOD_KEYWORD',
    'RETURN', 'ASYNC', 'AWAIT', 'DYN', 'BOX', 'RC', 'ARC', 'UNSAFE', 'LIFETIME', 'CONST', 'TYPE', 'WHERE', 'MOVE',
    'PUB', 'SUPER', 'SELF', 'LOOP', 'BREAK', 'CONTINUE', 'CLOSURE', 'PIPE', 'UNSAFE_FN',
    'COLON', 'COMMA', 'SEMICOLON', 'ARROW', 'FAT_ARROW', 'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE',
    'EQ', 'PLUS', 'MINUS', 'MULT', 'DIV', 'MOD', 'NUMBER', 'STRING', 'CHAR', 'BOOL', 'LBRACKET', 'RBRACKET', 'DOT',
    'AMP', 'AND', 'OR', 'TRUE', 'FALSE', 'NOT', 'LESS', 'GREATER', 'HASH', 'DOUBLECOLON', 'QUESTION_MARK',
    'UNDERSCORE', 'DERIVE', 'INLINE', 'EXCLAMATION_MARK', 'PLUS_EQ', 'MINUS_EQ', 'MULT_EQ', 'DIV_EQ', 'MOD_EQ',
    'SHL', 'SHR', 'BITAND', 'BITOR', 'BITXOR', 'SHL_EQ', 'SHR_EQ', 'TRAIT', 'BACKSLASH', 'NAME', 'STRING_LITERAL'
)

# キーワードを定義
keywords = {
    'extern': 'EXTERN',
    'crate': 'CRATE',
    'fn': 'FN',
    'let': 'LET',
    'mut': 'MUT',
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
    'for': 'FOR',
    'in': 'IN',
    'match': 'MATCH',
    'struct': 'STRUCT',
    'enum': 'ENUM',
    'impl': 'IMPL',
    'use': 'USE',
    'mod': 'MOD_KEYWORD',
    'return': 'RETURN',
    'async': 'ASYNC',
    'await': 'AWAIT',
    'dyn': 'DYN',
    'Box': 'BOX',
    'Rc': 'RC',
    'Arc': 'ARC',
    'unsafe': 'UNSAFE',
    'const': 'CONST',
    'type': 'TYPE',
    'where': 'WHERE',
    'move': 'MOVE',
    'pub': 'PUB',
    'super': 'SUPER',
    'self': 'SELF',
    'loop': 'LOOP',
    'break': 'BREAK',
    'continue': 'CONTINUE',
    'trait': 'TRAIT',
    'true': 'TRUE',
    'false': 'FALSE'
}


# 演算子や記号の定義
t_PLUS = r'\+'
t_MINUS = r'-'
t_MULT = r'\*'
t_DIV = r'/'
t_MOD = r'%'
t_EQ = r'='
t_LESS = r'<'
t_GREATER = r'>'
t_AMP = r'&'
t_AND = r'&&'
t_OR = r'\|\|'
t_NOT = r'!'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_COLON = r':'
t_COMMA = r','
t_SEMICOLON = r';'
t_ARROW = r'->'
t_FAT_ARROW = r'=>'
t_DOT = r'\.'
t_HASH = r'\#'
t_DOUBLECOLON = r'::'
t_QUESTION_MARK = r'\?'
# パイプとバックスラッシュのトークン定義を修正
t_PIPE = r'\|'
t_BACKSLASH = r'\\'

# 数値リテラル
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# 名前（識別子）を定義
def t_NAME(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = keywords.get(t.value, 'NAME')  # キーワードならトークンタイプを変更
    return t

# 文字列リテラル
def t_STRING(t):
    r'\".*?\"'
    t.value = t.value[1:-1]  # 文字列の両端の引用符を削除
    return t

# ライフタイム
def t_LIFETIME(t):
    r"'\w+"
    return t

# コメントと無視する文字
def t_COMMENT(t):
    r'//.*'
    pass

def t_MULTILINE_COMMENT(t):
    r'/\*[\s\S]*?\*/'
    pass

# 無視する文字（空白、タブ、改行）
t_ignore = ' \t'

# 改行の追跡
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# エラーハンドリング
def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

# 字句解析器の生成
lexer = lex.lex()