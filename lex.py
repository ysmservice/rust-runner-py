import ply.lex as lex

# トークンリスト
tokens = (
    'FN', 'LET', 'MUT', 'IF', 'ELSE', 'WHILE', 'FOR', 'IN', 'MATCH', 'STRUCT', 'ENUM', 'IMPL', 'USE', 'MOD', 'TRAIT',
    'RETURN', 'ASYNC', 'AWAIT', 'DYN', 'BOX', 'RC', 'ARC', 'UNSAFE', 'LIFETIME', 'CONST', 'TYPE', 'WHERE', 'MOVE',
    'EXTERN', 'CRATE', 'PUB', 'SUPER', 'SELF', 'LOOP', 'BREAK', 'CONTINUE', 'ASYNC_BLOCK', 'CLOSURE',
    'NAME', 'COLON', 'COMMA', 'SEMICOLON', 'ARROW', 'FAT_ARROW', 'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE',
    'EQ', 'PLUS', 'MINUS', 'MULT', 'DIV', 'NUMBER', 'STRING', 'CHAR', 'BOOL', 'LBRACKET', 'RBRACKET', 'DOT',
    'AMP', 'AND', 'OR', 'TRUE', 'FALSE', 'NOT', 'LESS', 'GREATER', 'HASH', 'DOUBLECOLON', 'QUESTION_MARK', 
    'UNDERSCORE', 'DERIVE', 'INLINE', 'ASYNC_BLOCK', 'EXCLAMATION_MARK', 'PLUS_EQ', 'MINUS_EQ', 'MULT_EQ',
    'DIV_EQ', 'MOD_EQ', 'SHL', 'SHR', 'MOD', 'BITAND', 'BITOR', 'BITXOR', 'SHL_EQ', 'SHR_EQ'
)

# トークンルールの正規表現
t_FN = r'fn'
t_LET = r'let'
t_MUT = r'mut'
t_IF = r'if'
t_ELSE = r'else'
t_WHILE = r'while'
t_FOR = r'for'
t_IN = r'in'
t_MATCH = r'match'
t_STRUCT = r'struct'
t_ENUM = r'enum'
t_IMPL = r'impl'
t_USE = r'use'
t_MOD = r'mod'
t_TRAIT = r'trait'
t_RETURN = r'return'
t_ASYNC = r'async'
t_AWAIT = r'await'
t_DYN = r'dyn'
t_BOX = r'Box'
t_RC = r'Rc'
t_ARC = r'Arc'
t_UNSAFE = r'unsafe'
t_CONST = r'const'
t_TYPE = r'type'
t_WHERE = r'where'
t_MOVE = r'move'
t_EXTERN = r'extern'
t_CRATE = r'crate'
t_PUB = r'pub'
t_SUPER = r'super'
t_SELF = r'self'
t_LOOP = r'loop'
t_BREAK = r'break'
t_CONTINUE = r'continue'

# 演算子と記号
t_EQ = r'='
t_PLUS = r'\+'
t_MINUS = r'-'
t_MULT = r'\*'
t_DIV = r'/'
t_MOD = r'%'
t_PLUS_EQ = r'\+='
t_MINUS_EQ = r'-='
t_MULT_EQ = r'\*='
t_DIV_EQ = r'/='
t_MOD_EQ = r'%='
t_SHL = r'<<'
t_SHR = r'>>'
t_SHL_EQ = r'<<='
t_SHR_EQ = r'>>='
t_AMP = r'&'
t_AND = r'&&'
t_OR = r'\|\|'
t_NOT = r'!'
t_BITAND = r'&'
t_BITOR = r'\|'
t_BITXOR = r'\^'

# カッコやその他の記号
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
t_EXCLAMATION_MARK = r'!'

# ブール値
t_TRUE = r'true'
t_FALSE = r'false'

# アトリビュート
t_DERIVE = r'#[derive\(.*\)]'
t_INLINE = r'#[inline]'

# 名前（識別子）
def t_NAME(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    return t

# ライフタイム
def t_LIFETIME(t):
    r"'\w+"
    return t

# 数値リテラル
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# 文字列リテラル
def t_STRING(t):
    r'\".*?\"'
    t.value = t.value[1:-1]  # 文字列の両端の引用符を削除
    return t

# 文字リテラル
def t_CHAR(t):
    r"'.'"
    t.value = t.value[1:-1]
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

# トークナイザーの生成
lexer = lex.lex()
