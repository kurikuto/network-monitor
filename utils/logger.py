"""
logger.py
ネットワーク接続情報をログファイルに保存するモジュール

CSV形式とJSON形式に対応しています。
"""

import csv
import json
from pathlib import Path
from datetime import datetime
import sys
import os

# 親ディレクトリをパスに追加
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.network_monitor import ConnectionInfo


class ConnectionLogger:
    """
    接続情報をファイルに保存するクラス
    
    CSV形式とJSON形式をサポートします。
    """
    
    def __init__(self, filepath: str, format: str = 'csv'):
        """
        初期化
        
        Args:
            filepath: 保存先ファイルパス
            format: 'csv' または 'json'
        """
        self.filepath = Path(filepath)
        self.format = format.lower()
        
        if self.format not in ['csv', 'json']:
            raise ValueError("format must be 'csv' or 'json'")
    
    def save(self, connections: list[ConnectionInfo], append: bool = False):
        """
        接続情報を保存
        
        Args:
            connections: 保存する接続情報のリスト
            append: True の場合は既存ファイルに追記
        """
        if not connections:
            print("保存する接続情報がありません。")
            return
        
        # ディレクトリが存在しない場合は作成
        self.filepath.parent.mkdir(parents=True, exist_ok=True)
        
        if self.format == 'csv':
            self._save_csv(connections, append)
        elif self.format == 'json':
            self._save_json(connections, append)
        
        print(f"✓ {len(connections)}件の接続情報を {self.filepath} に保存しました")
    
    def _save_csv(self, connections: list[ConnectionInfo], append: bool):
        """CSV形式で保存"""
        mode = 'a' if append else 'w'
        file_exists = self.filepath.exists()
        
        with open(self.filepath, mode, newline='', encoding='utf-8') as f:
            fieldnames = [
                'timestamp', 'process_name', 'pid', 
                'local_address', 'remote_address', 
                'protocol', 'status'
            ]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            
            # ヘッダーは新規作成時または既存ファイルが空の場合のみ書き込む
            if not append or not file_exists or self.filepath.stat().st_size == 0:
                writer.writeheader()
            
            for conn in connections:
                writer.writerow(conn.to_dict())
    
    def _save_json(self, connections: list[ConnectionInfo], append: bool):
        """JSON形式で保存"""
        data = [conn.to_dict() for conn in connections]
        
        if append and self.filepath.exists():
            # 既存データを読み込んで追記
            try:
                with open(self.filepath, 'r', encoding='utf-8') as f:
                    existing_data = json.load(f)
                    if isinstance(existing_data, list):
                        data = existing_data + data
            except json.JSONDecodeError:
                # 既存ファイルが不正な場合は上書き
                pass
        
        with open(self.filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def load(self) -> list[dict]:
        """
        保存されたログを読み込む
        
        Returns:
            接続情報の辞書リスト
        """
        if not self.filepath.exists():
            print(f"ファイルが見つかりません: {self.filepath}")
            return []
        
        if self.format == 'csv':
            return self._load_csv()
        elif self.format == 'json':
            return self._load_json()
    
    def _load_csv(self) -> list[dict]:
        """CSVファイルを読み込む"""
        data = []
        with open(self.filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                data.append(row)
        return data
    
    def _load_json(self) -> list[dict]:
        """JSONファイルを読み込む"""
        with open(self.filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data if isinstance(data, list) else [data]


# 簡易関数

def save_to_csv(connections: list[ConnectionInfo], filepath: str, append: bool = False):
    """
    CSV形式で保存（簡易版）
    
    Args:
        connections: 接続情報リスト
        filepath: 保存先パス
        append: 追記モード
    """
    logger = ConnectionLogger(filepath, 'csv')
    logger.save(connections, append)


def save_to_json(connections: list[ConnectionInfo], filepath: str, append: bool = False):
    """
    JSON形式で保存（簡易版）
    
    Args:
        connections: 接続情報リスト
        filepath: 保存先パス
        append: 追記モード
    """
    logger = ConnectionLogger(filepath, 'json')
    logger.save(connections, append)


# モジュール単体テスト
if __name__ == "__main__":
    from core.network_monitor import NetworkMonitor
    
    print("ネットワーク接続情報を取得してログ保存します...\n")
    
    # 接続情報を取得
    monitor = NetworkMonitor()
    connections = monitor.get_connections()
    
    # CSV保存
    print("CSV形式で保存:")
    save_to_csv(connections[:10], "test_log.csv")
    
    # JSON保存
    print("\nJSON形式で保存:")
    save_to_json(connections[:10], "test_log.json")
    
    # 読み込みテスト
    print("\nCSVファイルを読み込み:")
    csv_logger = ConnectionLogger("test_log.csv", "csv")
    loaded_data = csv_logger.load()
    print(f"読み込んだレコード数: {len(loaded_data)}")
    if loaded_data:
        print(f"最初のレコード: {loaded_data[0]}")
