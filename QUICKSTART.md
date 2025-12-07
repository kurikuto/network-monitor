# Network Monitor - クイックスタートガイド

## 🚀 インストールと実行

### 0. Python バージョンの確認

```powershell
python --version
# Python 3.9 以上が必要（Python 3.13 対応済み）
```

### 1. 仮想環境の作成（推奨）

仮想環境を使用することで、システムの Python 環境を汚さずにパッケージを管理できます。

#### Windows (PowerShell)

```powershell
# プロジェクトディレクトリに移動
cd network_monitor

# 仮想環境を作成
python -m venv venv

# 仮想環境を有効化
.\venv\Scripts\Activate.ps1

# ※ ExecutionPolicy エラーが出る場合
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### macOS / Linux

```bash
# プロジェクトディレクトリに移動
cd network_monitor

# 仮想環境を作成
python3 -m venv venv

# 仮想環境を有効化
source venv/bin/activate
```

仮想環境を無効化する場合：

```powershell
deactivate
```

### 2. 必要なパッケージをインストール

仮想環境を有効化した状態で：

```powershell
pip install -r requirements.txt

# または pyproject.toml を使用
pip install -e .
```

### 3. 基本的な実行

仮想環境を有効化した状態で：

```powershell
# 全接続を表示
python main.py

# 特定のプロセスのみ
python main.py --process chrome

# ポート443（HTTPS）の通信
python main.py --port 443

# リアルタイム監視（3秒ごと更新）
python main.py --watch 3
```

## 📝 よく使うコマンド例

```powershell
# ブラウザの通信を監視
python main.py --process "chrome,firefox,edge"

# HTTPS通信のみ
python main.py --port 443 --status ESTABLISHED

# サマリー表示
python main.py --summary

# CSV形式で保存
python main.py --log connections.csv

# IP逆引き（ホスト名表示）
python main.py --resolve --status ESTABLISHED
```

## 🖥️ GUI 版の起動

```powershell
# PyQt6が必要（初回のみ）
pip install PyQt6

# GUI版を起動
python ui/gui_app.py
```

## 📚 サンプルスクリプト

```powershell
# 基本的な使用例を実行
python examples/basic_usage.py
```

## ⚠️ トラブルシューティング

### 権限エラーが出る場合

Windows: PowerShell を管理者として実行

```powershell
Start-Process powershell -Verb RunAs
```

### 文字化けする場合

```powershell
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
chcp 65001
```

## 👨‍💻 開発者向け

### 型チェック

```powershell
pip install mypy
mypy core/ ui/ utils/ main.py
```

### コードフォーマットとリント

```powershell
pip install ruff
ruff check .
ruff format .
```

### pyproject.toml を使ったインストール

```powershell
pip install -e .
# または GUI も含めて
pip install -e ".[gui]"
# 開発ツールも含めて
pip install -e ".[dev,gui]"
```

## 🔧 カスタマイズ

各モジュールは独立しているので、自由に拡張できます：

- `core/network_monitor.py` - データ収集ロジック
- `ui/cli_display.py` - 表示形式
- `utils/filter.py` - フィルタリング条件
- `utils/logger.py` - ログ形式
- `utils/resolver.py` - DNS 逆引き

## 📚 詳細情報

- **README.md**: 詳細な機能説明とドキュメント
- **VIRTUAL_ENV.md**: 仮想環境の詳しい使い方
- **CHANGELOG.md**: 変更履歴とバージョン情報
