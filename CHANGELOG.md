# Changelog

## [1.0.0] - 2025-11-30

### ✨ Python 3.13 対応

#### 追加

- Python 3.9 以上に対応（Python 3.13 完全対応）
- `pyproject.toml` を追加して、モダンなパッケージ管理に対応
- セットアップ検証スクリプト `verify_setup.py` を追加

#### 変更

- **型ヒントの最新化**

  - `typing.List` → `list[]` (Python 3.9+のネイティブ型)
  - `typing.Dict` → `dict[]` (Python 3.9+のネイティブ型)
  - `typing.Set` → `set[]` (Python 3.9+のネイティブ型)
  - 不要な `typing` インポートを削除

- **依存パッケージの更新**

  - `psutil`: 5.9.0 → 6.1.0
  - `prettytable`: 3.9.0 → 3.12.0
  - `PyQt6`: 6.6.0 → 6.8.0 (オプション)

- **ドキュメントの更新**
  - README.md: Python 3.13 対応を明記
  - 学習ポイントに型ヒントに関する項目を追加
  - 開発者向けツール（mypy, ruff）の情報を追加

#### 技術的詳細

すべてのモジュールで型ヒントを Python 3.9+ のネイティブ型に更新：

- `core/network_monitor.py`
  - `List[ConnectionInfo]` → `list[ConnectionInfo]`
- `ui/cli_display.py`
  - `List[ConnectionInfo]` → `list[ConnectionInfo]`
- `utils/filter.py`
  - `List[str]`, `Set[str]`, `List[int]` → `list[str]`, `set[str]`, `list[int]`
  - すべてのフィルタメソッドと簡易関数を更新
- `utils/logger.py`
  - `List[ConnectionInfo]`, `List[dict]` → `list[ConnectionInfo]`, `list[dict]`
- `utils/resolver.py`
  - `Dict[str, str]` → `dict[str, str]`

#### 互換性

- **最小要件**: Python 3.9
- **推奨**: Python 3.11 以上
- **テスト済み**: Python 3.9, 3.10, 3.11, 3.12, 3.13
- **対応 OS**: Windows, macOS, Linux

#### 開発者向け改善

- 型チェックツール（mypy）のサポート
- コードフォーマッタ（ruff）のサポート
- `pyproject.toml` による統一的なプロジェクト設定

## 移行ガイド

既存の Python 3.8 環境から移行する場合：

```bash
# Python 3.9以上にアップグレード
python --version  # 3.9以上であることを確認

# 依存パッケージを更新
pip install -r requirements.txt --upgrade

# セットアップを検証
python verify_setup.py
```

型ヒントは後方互換性があるため、既存のコードは変更なしで動作します。
