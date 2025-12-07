"""
cli_display.py
コマンドライン上で接続情報を表形式で表示するモジュール

prettytableを使用して見やすい表形式で出力します。
"""

from prettytable import PrettyTable
import sys
import os

# 親ディレクトリをパスに追加（相対インポート用）
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.network_monitor import ConnectionInfo


class CLIDisplay:
    """
    CLI上でネットワーク接続情報を表示するクラス
    
    prettytableを使用して、整形された表形式で情報を出力します。
    """
    
    def __init__(self, show_timestamp: bool = False):
        """
        初期化
        
        Args:
            show_timestamp: タイムスタンプ列を表示するか
        """
        self.show_timestamp = show_timestamp
    
    def display_connections(self, connections: list[ConnectionInfo]):
        """
        接続情報を表形式で表示
        
        Args:
            connections: 表示する接続情報のリスト
        """
        if not connections:
            print("接続情報がありません。")
            return
        
        # テーブルの作成
        table = self._create_table()
        
        # データの追加
        for conn in connections:
            self._add_row(table, conn)
        
        # 表示
        print(table)
        print(f"\n総接続数: {len(connections)}")
    
    def _create_table(self) -> PrettyTable:
        """
        prettytableのテーブルオブジェクトを作成
        
        Returns:
            設定済みのPrettyTableオブジェクト
        """
        # カラム定義
        if self.show_timestamp:
            table = PrettyTable([
                "プロセス名", "PID", "ローカルアドレス", "リモートアドレス", 
                "プロトコル", "状態", "時刻"
            ])
        else:
            table = PrettyTable([
                "プロセス名", "PID", "ローカルアドレス", "リモートアドレス", 
                "プロトコル", "状態"
            ])
        
        # 表示設定
        table.align = "l"  # 左寄せ
        table.align["PID"] = "r"  # PIDは右寄せ
        
        return table
    
    def _add_row(self, table: PrettyTable, conn: ConnectionInfo):
        """
        テーブルに行を追加
        
        Args:
            table: PrettyTableオブジェクト
            conn: 追加する接続情報
        """
        # プロセス名を短縮（長すぎる場合）
        process_name = self._truncate_string(conn.process_name, 20)
        
        # 基本データ
        row_data = [
            process_name,
            conn.pid,
            conn.local_address,
            conn.remote_address,
            conn.protocol,
            conn.status
        ]
        
        # タイムスタンプを追加（オプション）
        if self.show_timestamp:
            row_data.append(conn.timestamp.strftime("%H:%M:%S"))
        
        table.add_row(row_data)
    
    def _truncate_string(self, text: str, max_length: int) -> str:
        """
        文字列を指定長で切り詰める
        
        Args:
            text: 対象文字列
            max_length: 最大文字数
            
        Returns:
            切り詰められた文字列
        """
        if len(text) <= max_length:
            return text
        return text[:max_length-3] + "..."
    
    def display_summary(self, connections: list[ConnectionInfo]):
        """
        接続情報のサマリーを表示
        
        Args:
            connections: 集計対象の接続情報リスト
        """
        if not connections:
            print("接続情報がありません。")
            return
        
        # 統計情報を集計
        total = len(connections)
        by_protocol = {}
        by_status = {}
        by_process = {}
        
        for conn in connections:
            # プロトコル別
            by_protocol[conn.protocol] = by_protocol.get(conn.protocol, 0) + 1
            
            # ステータス別
            by_status[conn.status] = by_status.get(conn.status, 0) + 1
            
            # プロセス別
            by_process[conn.process_name] = by_process.get(conn.process_name, 0) + 1
        
        # サマリー表示
        print("\n" + "="*60)
        print("接続サマリー")
        print("="*60)
        print(f"総接続数: {total}")
        
        # プロトコル別
        print("\n【プロトコル別】")
        proto_table = PrettyTable(["プロトコル", "接続数"])
        proto_table.align = "l"
        proto_table.align["接続数"] = "r"
        for protocol, count in sorted(by_protocol.items()):
            proto_table.add_row([protocol, count])
        print(proto_table)
        
        # ステータス別
        print("\n【状態別】")
        status_table = PrettyTable(["状態", "接続数"])
        status_table.align = "l"
        status_table.align["接続数"] = "r"
        for status, count in sorted(by_status.items(), key=lambda x: x[1], reverse=True):
            status_table.add_row([status, count])
        print(status_table)
        
        # プロセス別（上位10件）
        print("\n【プロセス別接続数 TOP10】")
        process_table = PrettyTable(["プロセス名", "接続数"])
        process_table.align = "l"
        process_table.align["接続数"] = "r"
        sorted_processes = sorted(by_process.items(), key=lambda x: x[1], reverse=True)
        for process, count in sorted_processes[:10]:
            process_table.add_row([process, count])
        print(process_table)
    
    def display_compact(self, connections: list[ConnectionInfo]):
        """
        コンパクトな形式で表示（スクリプトやログ向け）
        
        Args:
            connections: 表示する接続情報のリスト
        """
        for conn in connections:
            print(f"{conn.process_name}({conn.pid}): "
                  f"{conn.local_address} -> {conn.remote_address} "
                  f"[{conn.protocol}/{conn.status}]")


# モジュール単体テスト
if __name__ == "__main__":
    from core.network_monitor import NetworkMonitor
    
    print("ネットワーク接続情報を取得して表示します...\n")
    
    # 接続情報を取得
    monitor = NetworkMonitor()
    connections = monitor.get_connections()
    
    # 表示
    display = CLIDisplay(show_timestamp=True)
    display.display_connections(connections[:20])  # 最初の20件のみ
    
    # サマリー表示
    display.display_summary(connections)
