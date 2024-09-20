import os
import sys
import toml
import requests
from zipfile import ZipFile
import argparse
from parser import parser, lexer
import tarfile
from simulator import RustSimulator

# 依存関係をダウンロードするディレクトリ
MODULES_DIR = "rust_modules"

# 依存関係を解析する関数
def parse_cargo_toml(file_path):
    """Cargo.tomlから依存関係を解析"""
    if not os.path.exists(file_path):
        print(f"{file_path} が見つかりません")
        sys.exit(1)

    with open(file_path, 'r') as f:
        cargo_data = toml.load(f)
    
    dependencies = cargo_data.get("dependencies", {})
    return dependencies

# 依存関係をダウンロードする関数

def download_dependencies(dependencies):
    """依存関係をダウンロードして、rust_modulesフォルダに格納"""
    if not os.path.exists(MODULES_DIR):
        os.makedirs(MODULES_DIR)
    
    for dep_name, version_info in dependencies.items():
        if isinstance(version_info, str):
            version = version_info
        elif isinstance(version_info, dict):
            version = version_info.get("version", "")
        
        download_url = f"https://crates.io/api/v1/crates/{dep_name}/{version}/download"
        print(f"{dep_name} ({version}) をダウンロードしています: {download_url}")
        
        response = requests.get(download_url)
        if response.status_code == 200:
            # クレートファイルを保存
            file_path = os.path.join(MODULES_DIR, f"{dep_name}-{version}.crate")
            with open(file_path, 'wb') as f:
                f.write(response.content)
            
            # クレートファイルを展開
            if tarfile.is_tarfile(file_path):
                with tarfile.open(file_path, 'r:gz') as tar:
                    tar.extractall(path=os.path.join(MODULES_DIR, dep_name))
                os.remove(file_path)  # TARファイルを削除
                print(f"{dep_name} の展開が完了しました")
            else:
                print(f"{dep_name} はTARファイルではありません")
        else:
            print(f"{dep_name} のダウンロードに失敗しました")

# Rustファイルを解析し、シミュレーションを実行する関数
def simulate_rust_file(file_path):
    """指定されたRustファイルを解析してシミュレーションを実行"""
    print(f"{file_path} の解析を開始します")

    # Rustファイルの読み込み
    with open(file_path, 'r', encoding='utf-8') as f:
        rust_code = f.read()
    #lexer.input(rust_code)
    #for token in lexer:
    #    print(token)
    # Rustファイルの解析とシミュレーション（この部分はRust解析コードに依存）
    # パーサーを呼び出して、実際のRustコードの解析とシミュレーションを行う
    ast = parser.parse(rust_code, lexer=lexer)  # パーサーの呼び出し（parserは事前定義されたもの）
    
    # シミュレーターを使ってASTを評価し、結果を出力
    simulator = RustSimulator()  # Rust解析シミュレータのインスタンス化
    simulator.eval_ast(ast)  # ASTの評価

# メイン関数
def main():
    parser = argparse.ArgumentParser(description="Rustファイルの依存関係を解決して解析、シミュレーションを実行するスクリプト")
    parser.add_argument("rust_file", help="シミュレーションを実行するRustファイル")
    parser.add_argument("--no-download", action="store_true", help="依存関係をダウンロードしない")
    args = parser.parse_args()

    # Cargo.tomlの依存関係を解析
    cargo_toml_path = "Cargo.toml"
    dependencies = parse_cargo_toml(cargo_toml_path)

    # --no-downloadオプションが指定されていない場合、依存関係をダウンロード
    if not args.no_download:
        download_dependencies(dependencies)

    # Rustファイルを解析してシミュレーション実行
    simulate_rust_file(args.rust_file)

if __name__ == "__main__":
    main()
