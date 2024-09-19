import asyncio

class RustResult:
    def __init__(self, ok=None, err=None):
        self.ok = ok
        self.err = err

    def is_ok(self):
        return self.err is None

    def unwrap(self):
        if self.is_ok():
            return self.ok
        else:
            raise RuntimeError(f"Unwrapped error: {self.err}")

class RustSimulator:
    def __init__(self):
        # 変数、関数、所有権、ジェネリクスを管理
        self.variables = {}  # 変数の保存先
        self.functions = {}  # 関数の保存先
        self.ownership = {}  # 借用と所有権の追跡
        self.generic_types = {}  # ジェネリクス型の追跡

    def borrow_check(self, var_name):
        """借用チェックを実行"""
        if self.ownership.get(var_name) == 'moved':
            raise RuntimeError(f"変数 '{var_name}' はすでに所有権が移動されました")
    
    def move_variable(self, var_name):
        """変数の所有権を移動"""
        self.ownership[var_name] = 'moved'
    
    def eval_ast(self, node):
        """ASTノードを評価して実行"""
        node_type = node[0]

        if node_type == 'function':
            # 関数定義
            func_name = node[1]
            params = node[2]
            body = node[4]
            self.functions[func_name] = (params, body)
            print(f"Function '{func_name}' defined.")
        
        elif node_type == 'call':
            # 関数呼び出し
            func_name = node[1]
            args = [self.eval_ast(arg) for arg in node[2]]
            return self.call_function(func_name, args)

        elif node_type == 'let':
            # 変数定義
            var_name = node[1]
            value = self.eval_ast(node[2])
            self.variables[var_name] = value
            self.ownership[var_name] = 'owned'  # 所有権を設定
            print(f"Variable '{var_name}' = {value}")
        
        elif node_type == 'binary_op':
            # 二項演算（+,-,*,/など）
            left = self.eval_ast(node[1])
            right = self.eval_ast(node[3])
            operator = node[2]
            if operator == '+':
                return left + right
            elif operator == '-':
                return left - right
            elif operator == '*':
                return left * right
            elif operator == '/':
                return left / right
        
        elif node_type == 'if':
            # 条件文
            condition = self.eval_ast(node[1])
            if condition:
                return self.eval_ast(node[2])
            elif len(node) > 3 and node[3] is not None:
                return self.eval_ast(node[3])
        
        elif node_type == 'loop':
            # 無限ループ
            while True:
                result = self.eval_ast(node[1])
                if result == 'break':
                    break

        elif node_type == 'break':
            return 'break'

        elif node_type == 'identifier':
            # 変数の参照時に借用チェック
            var_name = node[1]
            self.borrow_check(var_name)
            return self.variables.get(var_name, None)

        elif node_type == 'number':
            # 数値リテラル
            return node[1]

        elif node_type == 'return':
            # 関数のリターン
            return self.eval_ast(node[1])

        elif node_type == 'move':
            # 所有権を移動する
            var_name = node[1]
            self.borrow_check(var_name)
            value = self.variables[var_name]
            self.move_variable(var_name)
            return value

        elif node_type == 'for':
            # forループのシミュレーション
            var_name = node[1]
            iterator = self.eval_ast(node[2])
            for value in iterator:
                self.variables[var_name] = value
                self.eval_ast(node[3])  # ループの本体

        elif node_type == 'range':
            # 範囲を生成
            start = self.eval_ast(node[1])
            end = self.eval_ast(node[2])
            return range(start, end)

        elif node_type == 'async':
            # 非同期関数の定義
            async_body = node[1]
            return asyncio.run(self.eval_async(async_body))

        elif node_type == 'match':
            # パターンマッチ
            match_expr = self.eval_ast(node[1])
            for pattern, body in node[2]:
                if self.match_pattern(pattern, match_expr):
                    return self.eval_ast(body)

        elif node_type == 'struct':
            # 構造体のインスタンス生成
            struct_name = node[1]
            fields = {k: self.eval_ast(v) for k, v in node[2].items()}
            return (struct_name, fields)

        elif node_type == 'result':
            # Result型のシミュレーション
            if node[1] == 'Ok':
                return RustResult(ok=self.eval_ast(node[2]))
            elif node[1] == 'Err':
                return RustResult(err=self.eval_ast(node[2]))

        elif node_type == 'generic_function':
            # ジェネリック型関数の定義
            func_name = node[1]
            generic_type = node[2]
            self.generic_types[func_name] = generic_type
            print(f"Generic function '{func_name}' with type '{generic_type}' defined.")

    async def eval_async(self, async_body):
        """非同期ブロックを実行"""
        result = self.eval_ast(async_body)
        await asyncio.sleep(1)  # 非同期処理の待機
        return result

    def call_function(self, func_name, args):
        """関数を実行"""
        if func_name not in self.functions:
            raise ValueError(f"Function '{func_name}' is not defined.")
        
        params, body = self.functions[func_name]
        local_variables = dict(zip(params, args))
        previous_variables = self.variables.copy()
        self.variables.update(local_variables)
        
        # 関数のボディを評価
        result = self.eval_ast(body)
        
        # グローバル変数を元に戻す
        self.variables = previous_variables
        return result

    def match_pattern(self, pattern, value):
        """パターンマッチングの実装"""
        if isinstance(pattern, tuple) and isinstance(value, tuple):
            if pattern[0] != value[0]:
                return False
            for p, v in zip(pattern[1], value[1]):
                if not self.match_pattern(p, v):
                    return False
            return True
        elif isinstance(pattern, str):
            return pattern == value
        else:
            return pattern == value
