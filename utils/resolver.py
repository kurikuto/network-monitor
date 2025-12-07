"""
resolver.py
IPアドレスを逆引きしてホスト名を取得するモジュール

DNSクエリを使用してIPアドレスのホスト名を解決します。
"""

import socket
from typing import Optional
from functools import lru_cache
import sys
import os

# 親ディレクトリをパスに追加
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class IPResolver:
    """
    IPアドレスをホスト名に解決するクラス
    
    キャッシュを使用して同じIPの繰り返しクエリを高速化します。
    """
    
    def __init__(self, timeout: float = 2.0):
        """
        初期化
        
        Args:
            timeout: DNS解決のタイムアウト（秒）
        """
        self.timeout = timeout
        self.cache: dict[str, str] = {}
    
    def resolve(self, ip_address: str) -> str:
        """
        IPアドレスをホスト名に解決
        
        Args:
            ip_address: 解決するIPアドレス
            
        Returns:
            ホスト名、解決できない場合は元のIPアドレス
        """
        # 特殊なケース
        if not ip_address or ip_address in ['*', '0.0.0.0', '::']:
            return ip_address
        
        # キャッシュチェック
        if ip_address in self.cache:
            return self.cache[ip_address]
        
        # 逆引き実行
        try:
            socket.setdefaulttimeout(self.timeout)
            hostname, _, _ = socket.gethostbyaddr(ip_address)
            self.cache[ip_address] = hostname
            return hostname
        except (socket.herror, socket.gaierror, socket.timeout):
            # 解決できない場合は元のIPを返す
            self.cache[ip_address] = ip_address
            return ip_address
        except Exception:
            return ip_address
    
    def resolve_address(self, address: str) -> str:
        """
        "ip:port" 形式のアドレスのIPをホスト名に解決
        
        Args:
            address: "ip:port" 形式の文字列
            
        Returns:
            "hostname:port" 形式の文字列
        """
        if not address or address == "*:*":
            return address
        
        try:
            # IPv6の場合: [::1]:8080
            if address.startswith('['):
                ip_end = address.index(']')
                ip = address[1:ip_end]
                port_part = address[ip_end+1:]
                hostname = self.resolve(ip)
                return f"[{hostname}]{port_part}"
            
            # IPv4の場合: 192.168.1.1:8080
            parts = address.rsplit(':', 1)
            if len(parts) == 2:
                ip, port = parts
                hostname = self.resolve(ip)
                return f"{hostname}:{port}"
            
        except Exception:
            pass
        
        return address
    
    def clear_cache(self):
        """キャッシュをクリア"""
        self.cache.clear()
    
    def get_cache_size(self) -> int:
        """キャッシュサイズを返す"""
        return len(self.cache)


# グローバルリゾルバ（簡易利用用）
_global_resolver = IPResolver()


def resolve_ip(ip_address: str) -> str:
    """
    IPアドレスを解決（グローバルリゾルバ使用）
    
    Args:
        ip_address: IPアドレス
        
    Returns:
        ホスト名
    """
    return _global_resolver.resolve(ip_address)


def resolve_address(address: str) -> str:
    """
    アドレス文字列を解決（グローバルリゾルバ使用）
    
    Args:
        address: "ip:port" 形式
        
    Returns:
        "hostname:port" 形式
    """
    return _global_resolver.resolve_address(address)


# モジュール単体テスト
if __name__ == "__main__":
    print("IP逆引きテスト\n")
    
    # テストIP
    test_ips = [
        "8.8.8.8",          # Google DNS
        "1.1.1.1",          # Cloudflare DNS
        "127.0.0.1",        # localhost
        "192.168.1.1",      # プライベートIP（解決できない可能性）
        "::1",              # IPv6 localhost
    ]
    
    resolver = IPResolver(timeout=3.0)
    
    print("IPアドレスの逆引き:")
    for ip in test_ips:
        hostname = resolver.resolve(ip)
        print(f"  {ip:20} -> {hostname}")
    
    print(f"\nキャッシュサイズ: {resolver.get_cache_size()}")
    
    # アドレス形式のテスト
    print("\nアドレス形式の逆引き:")
    test_addresses = [
        "8.8.8.8:443",
        "127.0.0.1:8080",
        "[::1]:3000",
    ]
    
    for addr in test_addresses:
        resolved = resolver.resolve_address(addr)
        print(f"  {addr:20} -> {resolved}")
