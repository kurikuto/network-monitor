# 仮想環境について

## 仮想環境とは？

Python の仮想環境（Virtual Environment）は、プロジェクトごとに独立した Python 環境を作成する仕組みです。

### メリット

1. **パッケージの分離**: プロジェクトごとに異なるバージョンのパッケージを使用できる
2. **システムの保護**: システム全体の Python 環境に影響を与えない
3. **再現性**: `requirements.txt`で環境を簡単に再現できる
4. **クリーンな環境**: 不要なパッケージが混入しない

## 基本的な使い方

### 作成と有効化

#### Windows (PowerShell)

```powershell
# 仮想環境を作成
python -m venv venv

# 有効化
.\venv\Scripts\Activate.ps1

# PowerShell の実行ポリシーエラーが出る場合
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### macOS / Linux

```bash
# 仮想環境を作成
python3 -m venv venv

# 有効化
source venv/bin/activate
```

### 確認方法

仮想環境が有効になると、プロンプトの先頭に `(venv)` が表示されます：

```powershell
(venv) PS C:\Users\k-ab6\Work\dev\python\network_monitor>
```

### パッケージのインストール

仮想環境を有効化した状態で：

```powershell
# requirements.txt からインストール
pip install -r requirements.txt

# 個別にインストール
pip install psutil prettytable

# インストール済みパッケージの確認
pip list
```

### 無効化

```powershell
deactivate
```

## 代替ツール

### 1. conda（Anaconda/Miniconda）

科学計算向けで、Python のバージョン管理も可能：

```bash
# 環境作成
conda create -n netmon python=3.13

# 有効化
conda activate netmon

# パッケージインストール
conda install psutil
pip install prettytable
```

### 2. Poetry

モダンなパッケージ管理ツール：

```bash
# Poetry のインストール
pip install poetry

# プロジェクト初期化
poetry install

# 仮想環境を有効化
poetry shell
```

### 3. pipenv

Pipfile を使った管理：

```bash
# pipenv のインストール
pip install pipenv

# 環境作成とパッケージインストール
pipenv install -r requirements.txt

# 仮想環境を有効化
pipenv shell
```

## このプロジェクトでの推奨手順

```powershell
# 1. プロジェクトディレクトリに移動
cd network_monitor

# 2. 仮想環境を作成
python -m venv venv

# 3. 有効化
.\venv\Scripts\Activate.ps1  # Windows
# source venv/bin/activate    # macOS/Linux

# 4. パッケージをインストール
pip install -r requirements.txt

# 5. セットアップを確認
python verify_setup.py

# 6. アプリケーションを実行
python main.py

# 7. 作業終了後は無効化
deactivate
```

## トラブルシューティング

### Windows で Activate.ps1 が実行できない

```powershell
# 現在のポリシーを確認
Get-ExecutionPolicy

# ポリシーを変更
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### venv フォルダを削除したい

```powershell
# Windows
Remove-Item -Recurse -Force venv

# macOS/Linux
rm -rf venv
```

### Python が見つからない

```powershell
# Python のパスを確認
where python     # Windows
which python3    # macOS/Linux

# venv 作成時に明示的にパスを指定
C:\Python313\python.exe -m venv venv
```

## .gitignore

仮想環境は Git で管理しません。`.gitignore` に追加済み：

```
venv/
env/
ENV/
```

## 参考リンク

- [Python 公式ドキュメント - venv](https://docs.python.org/ja/3/library/venv.html)
- [pip 公式ドキュメント](https://pip.pypa.io/en/stable/)
- [Python Packaging User Guide](https://packaging.python.org/)
