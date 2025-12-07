"""
basic_usage.py
基本的な使用例を示すサンプルスクリプト

このファイルを参考に、独自のスクリプトを作成できます。
"""

import sys
import os

# プロジェクトルートをパスに追加
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.network_monitor import NetworkMonitor
from ui.cli_display import CLIDisplay
from utils.filter import ConnectionFilter, filter_by_port, filter_by_status
from utils.logger import save_to_csv, save_to_json
from utils.resolver import IPResolver


def example1_basic_display():
    """例1: 基本的な表示"""
    print("=" * 70)
    print("例1: 全接続を表示")
    print("=" * 70)
    
    # 接続情報を取得
    monitor = NetworkMonitor()
    connections = monitor.get_connections()
    
    # 表示
    display = CLIDisplay()
    display.display_connections(connections[:10])  # 最初の10件のみ


def example2_filter_by_process():
    """例2: プロセス名でフィルタリング"""
    print("\n" + "=" * 70)
    print("例2: 特定プロセスの接続のみ表示")
    print("=" * 70)
    
    monitor = NetworkMonitor()
    connections = monitor.get_connections()
    
    # Pythonプロセスのみフィルタ
    conn_filter = ConnectionFilter()
    conn_filter.add_process_filter(['python', 'pythonw'])
    filtered = conn_filter.apply(connections)
    
    display = CLIDisplay()
    display.display_connections(filtered)


def example3_filter_https():
    """例3: HTTPS通信のみ表示"""
    print("\n" + "=" * 70)
    print("例3: HTTPS通信（ポート443）のみ表示")
    print("=" * 70)
    
    monitor = NetworkMonitor()
    connections = monitor.get_connections()
    
    # ポート443のみ
    https_connections = filter_by_port(connections, [443])
    
    display = CLIDisplay()
    display.display_connections(https_connections[:15])


def example4_active_connections():
    """例4: アクティブな接続のみ表示"""
    print("\n" + "=" * 70)
    print("例4: アクティブな接続（ESTABLISHED）のみ表示")
    print("=" * 70)
    
    monitor = NetworkMonitor()
    connections = monitor.get_connections()
    
    # ESTABLISHED状態のみ
    active = filter_by_status(connections, ['ESTABLISHED'])
    
    display = CLIDisplay()
    display.display_connections(active[:15])


def example5_summary():
    """例5: サマリー表示"""
    print("\n" + "=" * 70)
    print("例5: 接続サマリーを表示")
    print("=" * 70)
    
    monitor = NetworkMonitor()
    connections = monitor.get_connections()
    
    display = CLIDisplay()
    display.display_summary(connections)


def example6_save_log():
    """例6: ログ保存"""
    print("\n" + "=" * 70)
    print("例6: 接続情報をログファイルに保存")
    print("=" * 70)
    
    monitor = NetworkMonitor()
    connections = monitor.get_connections()
    
    # CSV形式で保存
    save_to_csv(connections[:20], "sample_connections.csv")
    
    # JSON形式で保存
    save_to_json(connections[:20], "sample_connections.json")


def example7_with_hostname():
    """例7: ホスト名解決"""
    print("\n" + "=" * 70)
    print("例7: IPアドレスをホスト名に解決して表示")
    print("=" * 70)
    
    monitor = NetworkMonitor()
    connections = monitor.get_connections()
    
    # ESTABLISHED状態のみ（時間短縮のため）
    active = filter_by_status(connections, ['ESTABLISHED'])[:5]
    
    # IP逆引き
    print("IPアドレスを逆引き中...")
    resolver = IPResolver(timeout=2.0)
    
    from core.network_monitor import ConnectionInfo
    resolved_connections = []
    for conn in active:
        resolved_conn = ConnectionInfo(
            process_name=conn.process_name,
            pid=conn.pid,
            local_address=resolver.resolve_address(conn.local_address),
            remote_address=resolver.resolve_address(conn.remote_address),
            protocol=conn.protocol,
            status=conn.status,
            timestamp=conn.timestamp
        )
        resolved_connections.append(resolved_conn)
    
    display = CLIDisplay()
    display.display_connections(resolved_connections)


def example8_complex_filter():
    """例8: 複合条件でのフィルタリング"""
    print("\n" + "=" * 70)
    print("例8: 複数条件でフィルタリング（TCP + ESTABLISHED）")
    print("=" * 70)
    
    monitor = NetworkMonitor()
    connections = monitor.get_connections()
    
    # TCPかつESTABLISHED状態
    conn_filter = ConnectionFilter()
    conn_filter.add_protocol_filter(['TCP'])
    conn_filter.add_status_filter(['ESTABLISHED'])
    
    filtered = conn_filter.apply(connections)
    
    display = CLIDisplay(show_timestamp=True)
    display.display_connections(filtered[:15])


def main():
    """サンプルを実行"""
    print("ネットワーク監視ツール - サンプルスクリプト")
    print("様々な使用例を実行します\n")
    
    try:
        # 各例を実行
        example1_basic_display()
        
        example2_filter_by_process()
        
        example3_filter_https()
        
        example4_active_connections()
        
        example5_summary()
        
        example6_save_log()
        
        example7_with_hostname()
        
        example8_complex_filter()
        
        print("\n" + "=" * 70)
        print("全てのサンプルが完了しました！")
        print("=" * 70)
        
    except KeyboardInterrupt:
        print("\n\n中断されました。")
    except PermissionError:
        print("\nエラー: 管理者権限が必要です。")
        print("Windows: 管理者としてコマンドプロンプトを起動してください")
        print("Linux/macOS: sudo を使用してください")
    except Exception as e:
        print(f"\nエラーが発生しました: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
