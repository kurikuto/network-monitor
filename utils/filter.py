"""
filter.py
接続情報のフィルタリング機能を提供するモジュール

プロセス名、ポート番号、プロトコル、状態などで
接続情報をフィルタリングできます。
"""

from typing import Optional
from collections.abc import Sequence
import re
import sys
import os

# 親ディレクトリをパスに追加
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.network_monitor import ConnectionInfo


class ConnectionFilter:
    """
    接続情報をフィルタリングするクラス
    
    複数の条件を組み合わせてフィルタリングが可能です。
    """
    
    def __init__(self):
        """初期化"""
        self.process_names: set[str] = set()
        self.ports: set[int] = set()
        self.protocols: set[str] = set()
        self.statuses: set[str] = set()
        self.pids: set[int] = set()
    
    def add_process_filter(self, process_names: list[str]) -> 'ConnectionFilter':
        """
        プロセス名フィルタを追加（部分一致）
        
        Args:
            process_names: フィルタリングするプロセス名のリスト
            
        Returns:
            self（メソッドチェーン用）
        """
        self.process_names.update([name.lower() for name in process_names])
        return self
    
    def add_port_filter(self, ports: list[int]) -> 'ConnectionFilter':
        """
        ポート番号フィルタを追加
        
        Args:
            ports: フィルタリングするポート番号のリスト
            
        Returns:
            self（メソッドチェーン用）
        """
        self.ports.update(ports)
        return self
    
    def add_protocol_filter(self, protocols: list[str]) -> 'ConnectionFilter':
        """
        プロトコルフィルタを追加
        
        Args:
            protocols: フィルタリングするプロトコルのリスト（例: ['TCP', 'UDP']）
            
        Returns:
            self（メソッドチェーン用）
        """
        self.protocols.update([proto.upper() for proto in protocols])
        return self
    
    def add_status_filter(self, statuses: list[str]) -> 'ConnectionFilter':
        """
        状態フィルタを追加
        
        Args:
            statuses: フィルタリングする状態のリスト（例: ['ESTABLISHED', 'LISTEN']）
            
        Returns:
            self（メソッドチェーン用）
        """
        self.statuses.update([status.upper() for status in statuses])
        return self
    
    def add_pid_filter(self, pids: list[int]) -> 'ConnectionFilter':
        """
        プロセスIDフィルタを追加
        
        Args:
            pids: フィルタリングするプロセスIDのリスト
            
        Returns:
            self（メソッドチェーン用）
        """
        self.pids.update(pids)
        return self
    
    def apply(self, connections: list[ConnectionInfo]) -> list[ConnectionInfo]:
        """
        フィルタを適用
        
        Args:
            connections: フィルタ対象の接続情報リスト
            
        Returns:
            フィルタリングされた接続情報リスト
        """
        filtered = connections
        
        # プロセス名フィルタ
        if self.process_names:
            filtered = [
                conn for conn in filtered
                if any(name in conn.process_name.lower() for name in self.process_names)
            ]
        
        # ポート番号フィルタ（ローカル・リモート両方をチェック）
        if self.ports:
            filtered = [
                conn for conn in filtered
                if self._check_port_match(conn)
            ]
        
        # プロトコルフィルタ
        if self.protocols:
            filtered = [
                conn for conn in filtered
                if conn.protocol.upper() in self.protocols
            ]
        
        # 状態フィルタ
        if self.statuses:
            filtered = [
                conn for conn in filtered
                if conn.status.upper() in self.statuses
            ]
        
        # PIDフィルタ
        if self.pids:
            filtered = [
                conn for conn in filtered
                if conn.pid in self.pids
            ]
        
        return filtered
    
    def _check_port_match(self, conn: ConnectionInfo) -> bool:
        """
        ポート番号が一致するかチェック
        
        Args:
            conn: チェック対象の接続情報
            
        Returns:
            一致すればTrue
        """
        # ローカルポートを抽出
        local_port = self._extract_port(conn.local_address)
        if local_port in self.ports:
            return True
        
        # リモートポートを抽出
        remote_port = self._extract_port(conn.remote_address)
        if remote_port in self.ports:
            return True
        
        return False
    
    def _extract_port(self, address: str) -> Optional[int]:
        """
        アドレス文字列からポート番号を抽出
        
        Args:
            address: "ip:port" 形式の文字列
            
        Returns:
            ポート番号、またはNone
        """
        try:
            # IPv6の場合: [::1]:8080 -> 8080
            # IPv4の場合: 192.168.1.1:8080 -> 8080
            if ':' in address:
                port_str = address.split(':')[-1]
                if port_str != '*' and port_str.isdigit():
                    return int(port_str)
        except:
            pass
        return None
    
    def clear(self):
        """全てのフィルタ条件をクリア"""
        self.process_names.clear()
        self.ports.clear()
        self.protocols.clear()
        self.statuses.clear()
        self.pids.clear()


# 便利な関数群

def filter_by_process(
    connections: list[ConnectionInfo], 
    process_names: list[str]
) -> list[ConnectionInfo]:
    """
    プロセス名でフィルタリング（簡易版）
    
    Args:
        connections: 接続情報リスト
        process_names: プロセス名リスト
        
    Returns:
        フィルタリングされた接続情報リスト
    """
    filter_obj = ConnectionFilter()
    filter_obj.add_process_filter(process_names)
    return filter_obj.apply(connections)


def filter_by_port(
    connections: list[ConnectionInfo], 
    ports: list[int]
) -> list[ConnectionInfo]:
    """
    ポート番号でフィルタリング（簡易版）
    
    Args:
        connections: 接続情報リスト
        ports: ポート番号リスト
        
    Returns:
        フィルタリングされた接続情報リスト
    """
    filter_obj = ConnectionFilter()
    filter_obj.add_port_filter(ports)
    return filter_obj.apply(connections)


def filter_by_protocol(
    connections: list[ConnectionInfo], 
    protocols: list[str]
) -> list[ConnectionInfo]:
    """
    プロトコルでフィルタリング（簡易版）
    
    Args:
        connections: 接続情報リスト
        protocols: プロトコルリスト
        
    Returns:
        フィルタリングされた接続情報リスト
    """
    filter_obj = ConnectionFilter()
    filter_obj.add_protocol_filter(protocols)
    return filter_obj.apply(connections)


def filter_by_status(
    connections: list[ConnectionInfo], 
    statuses: list[str]
) -> list[ConnectionInfo]:
    """
    状態でフィルタリング（簡易版）
    
    Args:
        connections: 接続情報リスト
        statuses: 状態リスト
        
    Returns:
        フィルタリングされた接続情報リスト
    """
    filter_obj = ConnectionFilter()
    filter_obj.add_status_filter(statuses)
    return filter_obj.apply(connections)


# モジュール単体テスト
if __name__ == "__main__":
    from core.network_monitor import NetworkMonitor
    from ui.cli_display import CLIDisplay
    
    print("ネットワーク接続を取得してフィルタリングします...\n")
    
    # 接続情報を取得
    monitor = NetworkMonitor()
    connections = monitor.get_connections()
    
    print(f"総接続数: {len(connections)}\n")
    
    # フィルタテスト1: ESTABLISHED状態のみ
    print("【ESTABLISHED状態のみ】")
    established = filter_by_status(connections, ['ESTABLISHED'])
    print(f"該当数: {len(established)}")
    
    # フィルタテスト2: TCPのみ
    print("\n【TCPプロトコルのみ】")
    tcp_only = filter_by_protocol(connections, ['TCP'])
    print(f"該当数: {len(tcp_only)}")
    
    # フィルタテスト3: ポート443（HTTPS）
    print("\n【ポート443の通信】")
    https_conns = filter_by_port(connections, [443])
    print(f"該当数: {len(https_conns)}")
    if https_conns:
        display = CLIDisplay()
        display.display_connections(https_conns[:10])
    
    # フィルタテスト4: 複合条件
    print("\n【複合条件: TCP + ESTABLISHED】")
    combined_filter = ConnectionFilter()
    combined_filter.add_protocol_filter(['TCP'])
    combined_filter.add_status_filter(['ESTABLISHED'])
    combined = combined_filter.apply(connections)
    print(f"該当数: {len(combined)}")
