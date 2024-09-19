import ply.lex as lex

# トークンリスト
tokens = (
    'FN', 'LET', 'MUT', 'IF', 'ELSE', 'WHILE', 'FOR', 'IN', 'MATCH', 'STRUCT', 'ENUM', 'IMPL', 'USE', 'MOD', 'TRAIT',
    'RETURN', 'ASYNC', 'AWAIT', 'DYN', 'BOX', 'RC', 'ARC', 'UNSAFE', 'LIFETIME', 'CONST', 'TYPE', 'WHERE', 'ASYNC',
    'MOVE', 'EXTERN', 'CRATE', 'PUB', 'SUPER', 'SELF', 'LOOP', 'BREAK', 'CONTINUE', 'ASYNC_BLOCK', 'CLOSURE',
    'NAME', 'COLON', 'COMMA', 'SEMICOLON', 'ARROW', 'FAT_ARROW', 'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE',
    'EQ', 'PLUS', 'MINUS', 'MULT', 'DIV', 'NUMBER', 'STRING', 'CHAR', 'BOOL', 'LBRACKET', 'RBRACKET', 'DOT',
    'AMP', 'AND', 'OR', 'TRUE', 'FALSE', 'NOT', 'LESS', 'GREATER', 'HASH', 'DOUBLECOLON', 'QUESTION_MARK', 
    'UNDERSCORE', 'DERIVE', 'INLINE', 'ASYNC_BLOCK'
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
t_LOOP = r'loop'
t_BREAK = r'break'
t_CONTINUE = r'continue'
t_DYN = r'dyn'
t_BOX = r'Box'
t_RC = r'Rc'
t_ARC = r'Arc'
t_UNSAFE = r'unsafe'
t_LIFETIME = r"'\w+"
t_CONST = r'const'
t_TYPE = r'type'
t_WHERE = r'where'
t_MOVE = r'move'
t_EXTERN = r'extern'
t_CRATE = r'crate'
t_PUB = r'pub'
t_SUPER = r'super'
t_SELF = r'self'

# 残りのトークンルールは省略（以前の例と同じ）
# ...

# 識別子とライフタイム
def t_NAME(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    return t

def t_LIFETIME(t):
    r"'\w+"
    t.value = t.value
    return t

# 数値
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# 無視する文字 (空白やタブ)
t_ignore = ' \t'

# 行数の追跡
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# エラーハンドリング
def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

# トークナイザーの生成
lexer = lex.lex()
