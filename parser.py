import ply.yacc as yacc
from lex import lexer , tokens

def p_start(p):
    '''start : statement_list'''
    p[0] = p[1]

def p_method_chain(p):
    '''method_chain : expression DOUBLECOLON NAME LPAREN param_list RPAREN
                    | expression DOUBLECOLON NAME LPAREN RPAREN
                    | expression DOT NAME LPAREN param_list RPAREN
                    | expression DOT NAME LPAREN RPAREN'''
    if len(p) == 6:
        p[0] = ('method_chain', p[1], p[3])
    else:
        p[0] = ('method_chain_with_params', p[1], p[3], p[5])

def p_function_call(p):
    '''function_call : NAME LPAREN param_list RPAREN
                     | NAME LPAREN RPAREN
                     | path DOUBLECOLON NAME LPAREN param_list RPAREN
                     | path DOUBLECOLON NAME LPAREN RPAREN'''
    if len(p) == 4:
        p[0] = ('function_call', p[1])
    elif len(p) == 5:
        p[0] = ('function_call', p[1], p[3])
    else:
        p[0] = ('function_call_with_params', p[1], p[3], p[5])

def p_use_declaration(p):
    '''use_declaration : USE path SEMICOLON
                       | USE path DOUBLECOLON MULT SEMICOLON'''  # グロブインポートを追加
    if len(p) == 4:
        p[0] = ('use_declaration', p[2])
    else:
        p[0] = ('use_glob_declaration', p[2])

def p_path(p):
    '''path : NAME
            | path DOUBLECOLON NAME'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ('path', p[1], p[3])

def p_const_declaration(p):
    '''const_declaration : CONST NAME COLON TYPE EQ expression SEMICOLON'''
    p[0] = ('const_declaration', p[2], p[4], p[6])

def p_impl_block(p):
    '''impl_block : IMPL NAME LBRACE statement_list RBRACE'''
    p[0] = ('impl_block', p[2], p[4])

def p_attribute(p):
    '''attribute : HASH LBRACKET NAME LPAREN NAME RPAREN RBRACKET'''
    p[0] = ('attribute', p[3], p[5])

# mod キーワードの構文ルールを追加
def p_mod_declaration(p):
    '''mod_declaration : MOD_KEYWORD NAME SEMICOLON
                       | MOD_KEYWORD NAME LBRACE statement_list RBRACE'''
    if len(p) == 4:
        p[0] = ('mod_declaration', p[2])
    else:
        p[0] = ('mod_declaration', p[2], p[4])

def p_extern_declaration(p):
    '''extern_declaration : EXTERN CRATE NAME SEMICOLON
                          | EXTERN STRING_LITERAL LBRACE extern_function_list RBRACE'''
    if len(p) == 4:
        p[0] = ('extern_declaration', p[3])
    else:
        p[0] = ('extern_block', p[2], p[4])

def p_extern_function_list(p):
    '''extern_function_list : extern_function
                            | extern_function extern_function_list
                            | empty'''
    if len(p) == 2:
        p[0] = [p[1]] if p[1] is not None else []
    elif len(p) == 3:
        p[0] = [p[1]] + p[2]

def p_extern_function(p):
    '''extern_function : FN NAME LPAREN RPAREN SEMICOLON'''
    p[0] = ('extern_function', p[2])

def p_param_list(p):
    '''param_list : param
                  | param COMMA param_list
                  | empty'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]

def p_param(p):
    '''param : NAME COLON TYPE'''
    p[0] = (p[1], p[3])

def p_statement_list(p):
    '''statement_list : statement
                      | statement statement_list'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[2]

def p_statement(p):
    '''statement : expression
                 | function
                 | loop_statement
                 | break_statement
                 | continue_statement
                 | extern_declaration
                 | mod_declaration
                 | const_declaration
                 | use_declaration
                 | method_chain
                 | function_call'''
    p[0] = p[1]


def p_lambda(p):
    '''LAMBDA : PIPE NAME PIPE'''
    p[0] = ('lambda', p[2])

def p_function(p):
    '''function : FN NAME LPAREN param_list RPAREN ARROW TYPE LBRACE statement_list RBRACE
                | UNSAFE_FN NAME LPAREN param_list RPAREN ARROW TYPE LBRACE statement_list RBRACE
                | ASYNC FN NAME LPAREN param_list RPAREN ARROW TYPE LBRACE statement_list RBRACE'''
    if len(p) == 11:
        p[0] = ('function', p[2], p[4], p[7], p[9])
    elif len(p) == 12:
        p[0] = ('unsafe_function', p[2], p[4], p[7], p[9])
    else:
        p[0] = ('async_function', p[3], p[5], p[8], p[10])

def p_loop_statement(p):
    '''loop_statement : LOOP LBRACE statement_list RBRACE'''
    p[0] = ('loop', p[3])

def p_break_statement(p):
    '''break_statement : BREAK SEMICOLON
                       | BREAK NAME SEMICOLON'''
    if len(p) == 3:
        p[0] = ('break',)
    else:
        p[0] = ('break', p[2])

def p_continue_statement(p):
    '''continue_statement : CONTINUE SEMICOLON
                          | CONTINUE NAME SEMICOLON'''
    if len(p) == 3:
        p[0] = ('continue',)
    else:
        p[0] = ('continue', p[2])

def p_closure(p):
    '''closure : LAMBDA param_list ARROW expression'''
    p[0] = ('closure', p[2], p[4])

def p_async_block(p):
    '''async_block : ASYNC LBRACE statement_list RBRACE'''
    p[0] = ('async_block', p[3])

def p_match_guard(p):
    '''match_guard : MATCH expression LBRACE match_arm_with_guard RBRACE'''
    p[0] = ('match_guard', p[2], p[4])

def p_match_arm_with_guard(p):
    '''match_arm_with_guard : pattern IF expression FAT_ARROW statement
                            | pattern FAT_ARROW statement'''
    if len(p) == 6:
        p[0] = (p[1], p[3], p[5])
    else:
        p[0] = (p[1], p[3])

# パターンマッチング
def p_match_statement(p):
    'match_statement : MATCH expression LBRACE match_arms RBRACE'
    p[0] = ('match', p[2], p[4])

def p_match_arms(p):
    '''match_arms : match_arm COMMA match_arms
                  | match_arm'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]

def p_match_arm(p):
    '''match_arm : pattern FAT_ARROW statement
                 | pattern FAT_ARROW LBRACE statement_list RBRACE'''
    if len(p) == 4:
        p[0] = (p[1], p[3])
    else:
        p[0] = (p[1], p[4])

def p_pattern(p):
    '''pattern : UNDERSCORE
               | NAME'''
    p[0] = p[1]

def p_expression(p):
    '''expression : NAME
                  | NUMBER
                  | STRING
                  | CHAR
                  | TRUE
                  | FALSE
                  | expression PLUS expression
                  | expression MINUS expression
                  | expression MULT expression
                  | expression DIV expression
                  | expression AND expression
                  | expression OR expression
                  | NOT expression
                  | AMP NAME
                  | AMP MUT NAME
                  | expression DOT NAME
                  | LPAREN expression COMMA expression RPAREN
                  | LBRACKET expression RBRACKET
                  | closure'''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 3:
        p[0] = ('not', p[2])
    elif len(p) == 4:
        if p[2] == '+':
            p[0] = ('+', p[1], p[3])
        elif p[2] == '-':
            p[0] = ('-', p[1], p[3])
        elif p[2] == '*':
            p[0] = ('*', p[1], p[3])
        elif p[2] == '/':
            p[0] = ('/', p[1], p[3])
        elif p[2] == '&&':
            p[0] = ('and', p[1], p[3])
        elif p[2] == '||':
            p[0] = ('or', p[1], p[3])
        elif p[2] == '.':
            p[0] = ('field_access', p[1], p[3])
    elif len(p) == 5:
        p[0] = ('tuple', p[2], p[4])

# 残りのルールは以前と同じ

def p_empty(p):
    'empty :'
    p[0] = None

def p_error(p):
    if p:
        print(f"Syntax error at '{p.value}' (line {p.lineno})")
    else:
        print("Syntax error at EOF")

# パーサーの生成
parser = yacc.yacc(debug=True)

# テスト用のRustコード
rust_code = """
use std::sync::Arc;

const MAX_POINTS: u32 = 100;

struct Point(i32, i32);

#[derive(Debug)]
struct Unit;

impl Point {
    fn new(x: i32, y: i32) -> Point {
        Point(x, y)
    }

    fn get_x(&self) -> i32 {
        self.0
    }
}

async fn async_func() {
    let num = 42;
    println!("Async value: {}", num);
}

fn main() {
    let p = Point::new(1, 2);
    println!("X: {}", p.get_x());

    let result: Result<i32, &str> = Ok(5);
    match result {
        Ok(val) => println!("Success: {}", val),
        Err(e) => println!("Error: {}", e),
    }

    loop {
        break;
    }

    let closure = |x| x + 1;
    let async_block = async { println!("Async block") };
}
"""

# パースの実行
#result = parser.parse(rust_code)
#print(result)
