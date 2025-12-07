# Network Monitor - ネットワーク通信可視化ツール

Python で作成したクロスプラットフォーム対応のネットワーク通信可視化ツールです。
OS やアプリケーションの通信状況をリアルタイムで確認できます。

## 📋 機能

### 基本機能

- ✅ プロセスごとの通信情報をリアルタイム表示
- ✅ プロセス名、PID、ローカル/リモート IP/ポート、プロトコル、状態を表示
- ✅ プロセス名やポート番号でフィルタリング
- ✅ 通信ログの保存（CSV/JSON 形式）

### 発展機能

- 🔄 IP アドレスの逆引き（ホスト名表示）
- 📊 通信統計の表示
- 🖥️ GUI 版（PyQt6 使用、オプション）

## 🚀 セットアップ

### 必要要件

- Python 3.9 以上（Python 3.13 対応済み）
- Windows / macOS / Linux

### インストール

1. リポジトリのクローン（または解凍）

```bash
cd network_monitor
```

2. 仮想環境の作成（推奨）

```bash
# Windows
python -m venv venv
.\venv\Scripts\Activate.ps1

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

3. 必要なパッケージのインストール

```bash
# requirements.txt を使用
pip install -r requirements.txt

# または pyproject.toml を使用（推奨）
pip install -e .
```

**注意**:

- Windows/macOS では一部のプロセス情報取得に管理者権限が必要な場合があります
- 仮想環境を使用することで、システム環境への影響を最小限に抑えられます

## 📖 使い方

### 基本的な使い方

全プロセスの通信状況を表示：

```bash
python main.py
```

### フィルタリング

特定のプロセスのみ表示：

```bash
python main.py --process chrome
```

特定のポートのみ表示：

```bash
python main.py --port 443
```

複数の条件でフィルタ：

```bash
python main.py --process firefox --port 80,443
```

### ログ保存

CSV 形式で保存：

```bash
python main.py --log network_log.csv
```

JSON 形式で保存：

```bash
python main.py --log network_log.json --format json
```

### リアルタイム監視

3 秒ごとに更新して監視：

```bash
python main.py --watch 3
```

### IP 逆引き

ホスト名を表示（処理が遅くなる場合があります）：

```bash
python main.py --resolve
```

## 📁 プロジェクト構成

```
network_monitor/
├── main.py                    # メインエントリーポイント
├── requirements.txt           # 必要なパッケージ一覧
├── pyproject.toml             # プロジェクト設定（モダンな方式）
├── README.md                  # このファイル
├── QUICKSTART.md              # クイックスタートガイド
├── VIRTUAL_ENV.md             # 仮想環境の詳細ガイド
├── CHANGELOG.md               # 変更履歴
├── verify_setup.py            # セットアップ検証スクリプト
│
├── core/                      # コア機能
│   ├── __init__.py
│   └── network_monitor.py     # ネットワーク情報収集
│
├── ui/                        # ユーザーインターフェース
│   ├── __init__.py
│   ├── cli_display.py         # CLI表示
│   └── gui_app.py             # GUI版（オプション）
│
├── utils/                     # ユーティリティ
│   ├── __init__.py
│   ├── filter.py              # フィルタリング機能
│   ├── logger.py              # ログ保存機能
│   └── resolver.py            # IP逆引き機能
│
└── examples/                  # サンプルスクリプト
    └── basic_usage.py         # 基本的な使用例
```

## 🔧 技術仕様

### 使用ライブラリ

- **psutil**: プロセスとネットワーク情報の取得
- **prettytable**: CLI 表形式表示
- **PyQt6**: GUI（オプション）

### 対応プロトコル

- TCP
- UDP
- TCP6（IPv6）
- UDP6（IPv6）

### 表示される接続状態

- ESTABLISHED（確立済み）
- LISTEN（待ち受け）
- TIME_WAIT（終了待ち）
- CLOSE_WAIT（切断待ち）
- など、OS がサポートする全ての状態

## 🎓 学習ポイント

このプロジェクトを通して学べること：

1. **ネットワーク基礎**

   - TCP/UDP の違い
   - ポート番号の役割
   - 接続状態の遷移

2. **Python プログラミング**

   - モジュール構成とパッケージ管理
   - クラス設計とオブジェクト指向
   - コマンドライン引数の処理
   - Python 3.9+ のネイティブ型ヒント (list[], dict[])
   - dataclass を使ったデータモデル

3. **システムプログラミング**
   - プロセス情報の取得
   - ネットワークソケットの理解
   - クロスプラットフォーム対応

## 📊 表示例

```
+--------+-------+-------------------+-------------------+----------+-------------+
|  Name  |  PID  |   Local Address   |  Remote Address   | Protocol |    State    |
+--------+-------+-------------------+-------------------+----------+-------------+
| chrome | 12345 | 192.168.1.5:54321 | 142.250.196.78:443|   TCP    | ESTABLISHED |
| firefox| 23456 | 192.168.1.5:54322 | 104.244.42.65:443 |   TCP    | ESTABLISHED |
| python | 34567 | 0.0.0.0:8000      |        *:*        |   TCP    |   LISTEN    |
+--------+-------+-------------------+-------------------+----------+-------------+
```

## 🛠️ カスタマイズ方法

### 独自のフィルタを追加

`utils/filter.py` に新しいフィルタ関数を追加できます。

### 表示項目の追加

`core/network_monitor.py` の `ConnectionInfo` クラスを拡張して、
帯域幅や累計データ量などの情報を追加できます。

### GUI 版の使用

```bash
python ui/gui_app.py
```

## ⚠️ 注意事項

- 一部のプロセス情報の取得には管理者権限が必要です
- Windows Defender などのセキュリティソフトで警告が出る場合があります
- 大量の接続がある場合、表示が遅くなることがあります

## 👨‍💻 開発者向け

### 型チェック

```bash
pip install mypy
mypy core/ ui/ utils/ main.py
```

### コードフォーマット

```bash
pip install ruff
ruff check .
ruff format .
```

## 🤝 貢献

機能追加やバグ修正の提案を歓迎します！

## 📄 ライセンス

MIT License

## 🔗 参考資料

- [psutil 公式ドキュメント](https://psutil.readthedocs.io/)
- [TCP/IP 基礎](https://ja.wikipedia.org/wiki/TCP/IP)
- [ポート番号一覧](https://ja.wikipedia.org/wiki/TCP/UDP%E3%83%9D%E3%83%BC%E3%83%88%E7%95%AA%E5%8F%B7%E3%81%AE%E4%B8%80%E8%A6%A7)
