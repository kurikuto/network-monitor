"""
network_monitor.py
ネットワーク接続情報を収集・管理するモジュール

このモジュールはpsutilを使用して、システム上の全プロセスの
ネットワーク接続情報を取得します。
"""

import psutil
from dataclasses import dataclass
from typing import Optional
from datetime import datetime
from collections.abc import Sequence


@dataclass
class ConnectionInfo:
    """
    個々のネットワーク接続情報を保持するデータクラス
    
    Attributes:
        process_name: プロセス名（例: "chrome.exe"）
        pid: プロセスID
        local_address: ローカルアドレス（IP:ポート）
        remote_address: リモートアドレス（IP:ポート）
        protocol: プロトコル（TCP/UDP/TCP6/UDP6）
        status: 接続状態（ESTABLISHED/LISTEN等）
        timestamp: 情報取得時刻
    """
    process_name: str
    pid: int
    local_address: str
    remote_address: str
    protocol: str
    status: str
    timestamp: datetime
    
    def to_dict(self) -> dict:
        """辞書形式に変換（ログ保存用）"""
        return {
            'process_name': self.process_name,
            'pid': self.pid,
            'local_address': self.local_address,
            'remote_address': self.remote_address,
            'protocol': self.protocol,
            'status': self.status,
            'timestamp': self.timestamp.isoformat()
        }


class NetworkMonitor:
    """
    ネットワーク接続を監視するメインクラス
    
    psutilを使用してシステム上の全ネットワーク接続を取得し、
    プロセス情報と組み合わせて詳細な接続情報を提供します。
    """
    
    def __init__(self):
        """初期化"""
        self.connections: list[ConnectionInfo] = []
    
    def get_connections(self) -> list[ConnectionInfo]:
        """
        現在の全ネットワーク接続を取得
        
        Returns:
            ConnectionInfo のリスト
        """
        self.connections = []
        timestamp = datetime.now()
        
        # 全プロセスを走査
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                # プロセスのネットワーク接続を取得
                connections = proc.net_connections(kind='inet')
                
                for conn in connections:
                    # 接続情報を構築
                    conn_info = self._create_connection_info(
                        proc, conn, timestamp
                    )
                    if conn_info:
                        self.connections.append(conn_info)
                        
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                # アクセス権限がない、またはプロセスが終了した場合はスキップ
                continue
            except Exception as e:
                # その他のエラーも静かにスキップ
                continue
        
        return self.connections
    
    def _create_connection_info(
        self, 
        proc: psutil.Process, 
        conn: psutil._common.sconn,
        timestamp: datetime
    ) -> Optional[ConnectionInfo]:
        """
        プロセスとコネクション情報からConnectionInfoを作成
        
        Args:
            proc: psutilのProcessオブジェクト
            conn: psutilのsconnオブジェクト
            timestamp: タイムスタンプ
            
        Returns:
            ConnectionInfo または None
        """
        try:
            # プロセス情報
            process_name = proc.info['name']
            pid = proc.info['pid']
            
            # プロトコル判定
            protocol = self._get_protocol_name(conn)
            
            # ローカルアドレス
            local_addr = self._format_address(conn.laddr)
            
            # リモートアドレス
            if conn.raddr:
                remote_addr = self._format_address(conn.raddr)
            else:
                remote_addr = "*:*"
            
            # ステータス（UDPの場合は"NONE"になる）
            status = conn.status if conn.status else "NONE"
            
            return ConnectionInfo(
                process_name=process_name,
                pid=pid,
                local_address=local_addr,
                remote_address=remote_addr,
                protocol=protocol,
                status=status,
                timestamp=timestamp
            )
            
        except Exception:
            return None
    
    def _get_protocol_name(self, conn: psutil._common.sconn) -> str:
        """
        接続オブジェクトからプロトコル名を取得
        
        Args:
            conn: psutilのsconnオブジェクト
            
        Returns:
            プロトコル名（TCP/UDP/TCP6/UDP6）
        """
        family = conn.family
        conn_type = conn.type
        
        # ファミリーとタイプから判定
        import socket
        
        if family == socket.AF_INET:
            if conn_type == socket.SOCK_STREAM:
                return "TCP"
            elif conn_type == socket.SOCK_DGRAM:
                return "UDP"
        elif family == socket.AF_INET6:
            if conn_type == socket.SOCK_STREAM:
                return "TCP6"
            elif conn_type == socket.SOCK_DGRAM:
                return "UDP6"
        
        return "UNKNOWN"
    
    def _format_address(self, addr) -> str:
        """
        アドレスタプルを文字列に変換
        
        Args:
            addr: (ip, port) のタプル
            
        Returns:
            "ip:port" 形式の文字列
        """
        if not addr:
            return "*:*"
        
        ip = addr[0] if addr[0] else "*"
        port = addr[1] if len(addr) > 1 else "*"
        
        # IPv6アドレスの場合は []で囲む
        if ':' in str(ip) and not ip.startswith('['):
            ip = f"[{ip}]"
        
        return f"{ip}:{port}"
    
    def get_connection_count(self) -> int:
        """現在の接続数を返す"""
        return len(self.connections)
    
    def get_active_connections(self) -> list[ConnectionInfo]:
        """アクティブな接続（ESTABLISHED状態）のみ返す"""
        return [
            conn for conn in self.connections 
            if conn.status == "ESTABLISHED"
        ]
    
    def get_listening_connections(self) -> list[ConnectionInfo]:
        """待ち受け中の接続（LISTEN状態）のみ返す"""
        return [
            conn for conn in self.connections 
            if conn.status == "LISTEN"
        ]


# 使用例
if __name__ == "__main__":
    # モジュール単体でのテスト実行
    print("ネットワーク接続を取得中...")
    
    monitor = NetworkMonitor()
    connections = monitor.get_connections()
    
    print(f"\n取得した接続数: {len(connections)}")
    print(f"アクティブな接続: {len(monitor.get_active_connections())}")
    print(f"待ち受け中: {len(monitor.get_listening_connections())}")
    
    # 最初の5件を表示
    print("\n最初の5件:")
    for i, conn in enumerate(connections[:5], 1):
        print(f"{i}. {conn.process_name} (PID:{conn.pid})")
        print(f"   {conn.local_address} -> {conn.remote_address}")
        print(f"   {conn.protocol} [{conn.status}]")
