#!/usr/bin/env python3
"""
main.py
ネットワーク通信可視化ツールのメインエントリーポイント

コマンドライン引数を処理し、適切なモジュールを呼び出します。
"""

import argparse
import sys
import time
import os
from datetime import datetime

# モジュールのインポート
from core.network_monitor import NetworkMonitor
from ui.cli_display import CLIDisplay
from utils.filter import ConnectionFilter
from utils.logger import ConnectionLogger
from utils.resolver import IPResolver


def parse_arguments():
    """コマンドライン引数を解析"""
    parser = argparse.ArgumentParser(
        description='ネットワーク通信可視化ツール - プロセスごとの通信情報を表示',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:
  python main.py                           # 全接続を表示
  python main.py --process chrome          # chromeの接続のみ表示
  python main.py --port 443,80             # ポート443,80の接続を表示
  python main.py --protocol TCP            # TCPのみ表示
  python main.py --status ESTABLISHED      # ESTABLISHED状態のみ表示
  python main.py --watch 3                 # 3秒ごとに更新
  python main.py --log connections.csv     # CSV形式で保存
  python main.py --resolve                 # IPをホスト名に解決
  python main.py --summary                 # サマリー表示
        """
    )
    
    # フィルタオプション
    filter_group = parser.add_argument_group('フィルタオプション')
    filter_group.add_argument(
        '--process', '-p',
        help='プロセス名でフィルタ（部分一致、カンマ区切りで複数指定可）'
    )
    filter_group.add_argument(
        '--port',
        help='ポート番号でフィルタ（カンマ区切りで複数指定可）'
    )
    filter_group.add_argument(
        '--protocol',
        choices=['TCP', 'UDP', 'TCP6', 'UDP6'],
        help='プロトコルでフィルタ'
    )
    filter_group.add_argument(
        '--status',
        choices=['ESTABLISHED', 'LISTEN', 'TIME_WAIT', 'CLOSE_WAIT', 'SYN_SENT', 'SYN_RECV'],
        help='接続状態でフィルタ'
    )
    filter_group.add_argument(
        '--pid',
        type=int,
        help='プロセスIDでフィルタ'
    )
    
    # 表示オプション
    display_group = parser.add_argument_group('表示オプション')
    display_group.add_argument(
        '--summary', '-s',
        action='store_true',
        help='サマリー表示モード'
    )
    display_group.add_argument(
        '--compact', '-c',
        action='store_true',
        help='コンパクト表示モード'
    )
    display_group.add_argument(
        '--limit', '-l',
        type=int,
        help='表示件数を制限'
    )
    display_group.add_argument(
        '--timestamp', '-t',
        action='store_true',
        help='タイムスタンプを表示'
    )
    
    # 機能オプション
    func_group = parser.add_argument_group('機能オプション')
    func_group.add_argument(
        '--watch', '-w',
        type=int,
        metavar='SECONDS',
        help='指定秒数ごとに自動更新（リアルタイム監視）'
    )
    func_group.add_argument(
        '--log',
        help='ログファイルに保存（拡張子: .csv または .json）'
    )
    func_group.add_argument(
        '--format',
        choices=['csv', 'json'],
        default='csv',
        help='ログ保存形式（デフォルト: csv）'
    )
    func_group.add_argument(
        '--append',
        action='store_true',
        help='既存ログファイルに追記'
    )
    func_group.add_argument(
        '--resolve', '-r',
        action='store_true',
        help='IPアドレスをホスト名に解決（処理が遅くなります）'
    )
    
    return parser.parse_args()


def apply_filters(connections, args):
    """引数に基づいてフィルタを適用"""
    conn_filter = ConnectionFilter()
    
    # プロセス名フィルタ
    if args.process:
        processes = [p.strip() for p in args.process.split(',')]
        conn_filter.add_process_filter(processes)
    
    # ポート番号フィルタ
    if args.port:
        try:
            ports = [int(p.strip()) for p in args.port.split(',')]
            conn_filter.add_port_filter(ports)
        except ValueError:
            print("エラー: ポート番号は整数で指定してください", file=sys.stderr)
            sys.exit(1)
    
    # プロトコルフィルタ
    if args.protocol:
        conn_filter.add_protocol_filter([args.protocol])
    
    # ステータスフィルタ
    if args.status:
        conn_filter.add_status_filter([args.status])
    
    # PIDフィルタ
    if args.pid:
        conn_filter.add_pid_filter([args.pid])
    
    return conn_filter.apply(connections)


def resolve_connections(connections, resolver):
    """接続情報のIPアドレスをホスト名に解決"""
    from core.network_monitor import ConnectionInfo
    
    resolved_connections = []
    for conn in connections:
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
    
    return resolved_connections


def clear_screen():
    """画面をクリア"""
    os.system('cls' if os.name == 'nt' else 'clear')


def main():
    """メイン処理"""
    args = parse_arguments()
    
    # ネットワークモニターの初期化
    monitor = NetworkMonitor()
    
    # ディスプレイの初期化
    display = CLIDisplay(show_timestamp=args.timestamp)
    
    # IP逆引き用リゾルバ
    resolver = IPResolver() if args.resolve else None
    
    # ログ保存設定
    logger = None
    if args.log:
        # ファイル拡張子から形式を自動判定
        if args.log.endswith('.json'):
            log_format = 'json'
        elif args.log.endswith('.csv'):
            log_format = 'csv'
        else:
            log_format = args.format
        
        logger = ConnectionLogger(args.log, log_format)
    
    try:
        # ウォッチモード
        if args.watch:
            print(f"リアルタイム監視モード（{args.watch}秒ごとに更新）")
            print("終了するには Ctrl+C を押してください\n")
            
            iteration = 0
            while True:
                clear_screen()
                
                # 現在時刻を表示
                print(f"更新: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                print("="*70)
                
                # 接続情報を取得
                connections = monitor.get_connections()
                
                # フィルタ適用
                connections = apply_filters(connections, args)
                
                # IP逆引き
                if resolver:
                    connections = resolve_connections(connections, resolver)
                
                # 件数制限
                if args.limit:
                    connections = connections[:args.limit]
                
                # 表示
                if args.summary:
                    display.display_summary(connections)
                elif args.compact:
                    display.display_compact(connections)
                else:
                    display.display_connections(connections)
                
                # ログ保存
                if logger and iteration > 0:  # 最初の実行後から保存
                    logger.save(connections, append=args.append)
                
                iteration += 1
                time.sleep(args.watch)
                
        # 通常モード（1回のみ実行）
        else:
            print("ネットワーク接続情報を取得中...")
            
            # 接続情報を取得
            connections = monitor.get_connections()
            
            # フィルタ適用
            connections = apply_filters(connections, args)
            
            # IP逆引き
            if resolver:
                print("IPアドレスを逆引き中...")
                connections = resolve_connections(connections, resolver)
            
            # 件数制限
            if args.limit:
                connections = connections[:args.limit]
            
            print()  # 空行
            
            # 表示
            if args.summary:
                display.display_summary(connections)
            elif args.compact:
                display.display_compact(connections)
            else:
                display.display_connections(connections)
            
            # ログ保存
            if logger:
                logger.save(connections, append=args.append)
    
    except KeyboardInterrupt:
        print("\n\n中断されました。")
        sys.exit(0)
    except PermissionError:
        print("\nエラー: 管理者権限が必要です。", file=sys.stderr)
        print("Windowsの場合: 管理者としてコマンドプロンプトを起動してください", file=sys.stderr)
        print("Linux/macOSの場合: sudo を使用してください", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"\nエラーが発生しました: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
