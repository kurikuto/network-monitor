"""
verify_setup.py
セットアップと環境の検証スクリプト

Python 3.13対応のために必要な依存関係を確認します。
"""

import sys
import importlib.util


def check_python_version():
    """Python バージョンをチェック"""
    version = sys.version_info
    print(f"✓ Python バージョン: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 9):
        print("✗ エラー: Python 3.9 以上が必要です")
        return False
    
    if version.major == 3 and version.minor >= 13:
        print("  → Python 3.13+ 対応済み")
    
    return True


def check_module(module_name: str, friendly_name: str = None) -> bool:
    """モジュールのインストール状態をチェック"""
    if friendly_name is None:
        friendly_name = module_name
    
    spec = importlib.util.find_spec(module_name)
    if spec is None:
        print(f"✗ {friendly_name} がインストールされていません")
        return False
    else:
        try:
            module = importlib.import_module(module_name)
            version = getattr(module, '__version__', 'バージョン不明')
            print(f"✓ {friendly_name}: {version}")
            return True
        except Exception as e:
            print(f"⚠ {friendly_name}: インポートエラー ({e})")
            return False


def check_type_hints():
    """型ヒントの動作確認"""
    print("\n型ヒント機能の確認:")
    
    try:
        # Python 3.9+ のネイティブ型ヒント
        test_list: list[str] = ["test"]
        test_dict: dict[str, int] = {"key": 1}
        print("✓ Python 3.9+ ネイティブ型ヒント (list[], dict[]) が利用可能")
        return True
    except Exception as e:
        print(f"✗ 型ヒントエラー: {e}")
        return False


def check_project_files():
    """プロジェクトファイルの存在確認"""
    import os
    from pathlib import Path
    
    print("\nプロジェクトファイルの確認:")
    
    required_files = [
        "main.py",
        "requirements.txt",
        "README.md",
        "pyproject.toml",
        "core/network_monitor.py",
        "ui/cli_display.py",
        "utils/filter.py",
        "utils/logger.py",
        "utils/resolver.py",
    ]
    
    all_exist = True
    for file in required_files:
        file_path = Path(file)
        if file_path.exists():
            print(f"✓ {file}")
        else:
            print(f"✗ {file} が見つかりません")
            all_exist = False
    
    return all_exist


def main():
    """メイン処理"""
    print("=" * 70)
    print("Network Monitor - セットアップ検証")
    print("=" * 70)
    
    print("\nPython バージョン確認:")
    python_ok = check_python_version()
    
    print("\n必須パッケージの確認:")
    psutil_ok = check_module("psutil", "psutil")
    prettytable_ok = check_module("prettytable", "prettytable")
    
    print("\nオプショナルパッケージの確認:")
    pyqt_ok = check_module("PyQt6", "PyQt6 (GUI用)")
    if not pyqt_ok:
        print("  → GUI版を使用する場合: pip install PyQt6")
    
    mypy_ok = check_module("mypy", "mypy (型チェック用)")
    if not mypy_ok:
        print("  → 型チェックを使用する場合: pip install mypy")
    
    ruff_ok = check_module("ruff", "ruff (コードフォーマット用)")
    if not ruff_ok:
        print("  → コードフォーマットを使用する場合: pip install ruff")
    
    type_hints_ok = check_type_hints()
    
    files_ok = check_project_files()
    
    print("\n" + "=" * 70)
    print("検証結果:")
    print("=" * 70)
    
    if python_ok and psutil_ok and prettytable_ok and type_hints_ok and files_ok:
        print("✓ 全ての必須要件が満たされています！")
        print("\n次のコマンドで実行できます:")
        print("  python main.py")
        return 0
    else:
        print("✗ いくつかの問題があります。上記のエラーを確認してください。")
        print("\n必須パッケージをインストールするには:")
        print("  pip install -r requirements.txt")
        return 1


if __name__ == "__main__":
    sys.exit(main())
