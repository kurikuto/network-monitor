"""
gui_app.py
PyQt6を使用したGUI版ネットワーク監視ツール

※ このファイルを使用するには PyQt6 のインストールが必要です:
  pip install PyQt6

基本的なGUI実装のサンプルです。必要に応じてカスタマイズしてください。
"""

try:
    from PyQt6.QtWidgets import (
        QApplication, QMainWindow, QTableWidget, QTableWidgetItem,
        QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QLineEdit,
        QLabel, QComboBox, QStatusBar, QMessageBox
    )
    from PyQt6.QtCore import QTimer, Qt
    PYQT_AVAILABLE = True
except ImportError:
    PYQT_AVAILABLE = False
    print("PyQt6がインストールされていません。")
    print("インストール方法: pip install PyQt6")

import sys
import os

# 親ディレクトリをパスに追加
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.network_monitor import NetworkMonitor
from utils.filter import ConnectionFilter


if PYQT_AVAILABLE:
    class NetworkMonitorGUI(QMainWindow):
        """ネットワーク監視GUIアプリケーション"""
        
        def __init__(self):
            super().__init__()
            self.monitor = NetworkMonitor()
            self.conn_filter = ConnectionFilter()
            self.auto_refresh = False
            
            self.init_ui()
            self.setup_timer()
            self.refresh_data()
        
        def init_ui(self):
            """UIの初期化"""
            self.setWindowTitle('ネットワーク通信監視ツール')
            self.setGeometry(100, 100, 1200, 700)
            
            # 中央ウィジェット
            central_widget = QWidget()
            self.setCentralWidget(central_widget)
            
            # メインレイアウト
            main_layout = QVBoxLayout()
            central_widget.setLayout(main_layout)
            
            # フィルタ部分
            filter_layout = self.create_filter_section()
            main_layout.addLayout(filter_layout)
            
            # テーブル
            self.table = QTableWidget()
            self.setup_table()
            main_layout.addWidget(self.table)
            
            # ボタン部分
            button_layout = self.create_button_section()
            main_layout.addLayout(button_layout)
            
            # ステータスバー
            self.statusBar = QStatusBar()
            self.setStatusBar(self.statusBar)
            self.statusBar.showMessage('準備完了')
        
        def create_filter_section(self):
            """フィルタセクションを作成"""
            layout = QHBoxLayout()
            
            # プロセス名フィルタ
            layout.addWidget(QLabel('プロセス:'))
            self.process_input = QLineEdit()
            self.process_input.setPlaceholderText('例: chrome, firefox')
            layout.addWidget(self.process_input)
            
            # ポート番号フィルタ
            layout.addWidget(QLabel('ポート:'))
            self.port_input = QLineEdit()
            self.port_input.setPlaceholderText('例: 443, 80')
            layout.addWidget(self.port_input)
            
            # プロトコルフィルタ
            layout.addWidget(QLabel('プロトコル:'))
            self.protocol_combo = QComboBox()
            self.protocol_combo.addItems(['全て', 'TCP', 'UDP', 'TCP6', 'UDP6'])
            layout.addWidget(self.protocol_combo)
            
            # 状態フィルタ
            layout.addWidget(QLabel('状態:'))
            self.status_combo = QComboBox()
            self.status_combo.addItems([
                '全て', 'ESTABLISHED', 'LISTEN', 'TIME_WAIT', 
                'CLOSE_WAIT', 'SYN_SENT'
            ])
            layout.addWidget(self.status_combo)
            
            # フィルタ適用ボタン
            filter_btn = QPushButton('フィルタ適用')
            filter_btn.clicked.connect(self.apply_filter)
            layout.addWidget(filter_btn)
            
            return layout
        
        def create_button_section(self):
            """ボタンセクションを作成"""
            layout = QHBoxLayout()
            
            # 更新ボタン
            refresh_btn = QPushButton('手動更新')
            refresh_btn.clicked.connect(self.refresh_data)
            layout.addWidget(refresh_btn)
            
            # 自動更新トグル
            self.auto_refresh_btn = QPushButton('自動更新 開始')
            self.auto_refresh_btn.clicked.connect(self.toggle_auto_refresh)
            layout.addWidget(self.auto_refresh_btn)
            
            # クリアボタン
            clear_btn = QPushButton('フィルタクリア')
            clear_btn.clicked.connect(self.clear_filters)
            layout.addWidget(clear_btn)
            
            layout.addStretch()
            
            # 接続数表示
            self.count_label = QLabel('接続数: 0')
            layout.addWidget(self.count_label)
            
            return layout
        
        def setup_table(self):
            """テーブルの設定"""
            headers = [
                'プロセス名', 'PID', 'ローカルアドレス', 
                'リモートアドレス', 'プロトコル', '状態'
            ]
            self.table.setColumnCount(len(headers))
            self.table.setHorizontalHeaderLabels(headers)
            
            # 列幅の調整
            self.table.setColumnWidth(0, 150)
            self.table.setColumnWidth(1, 80)
            self.table.setColumnWidth(2, 200)
            self.table.setColumnWidth(3, 200)
            self.table.setColumnWidth(4, 100)
            self.table.setColumnWidth(5, 120)
        
        def setup_timer(self):
            """自動更新タイマーの設定"""
            self.timer = QTimer()
            self.timer.timeout.connect(self.refresh_data)
        
        def apply_filter(self):
            """フィルタを適用"""
            self.conn_filter.clear()
            
            # プロセス名
            process_text = self.process_input.text().strip()
            if process_text:
                processes = [p.strip() for p in process_text.split(',')]
                self.conn_filter.add_process_filter(processes)
            
            # ポート番号
            port_text = self.port_input.text().strip()
            if port_text:
                try:
                    ports = [int(p.strip()) for p in port_text.split(',')]
                    self.conn_filter.add_port_filter(ports)
                except ValueError:
                    QMessageBox.warning(
                        self, '入力エラー', 
                        'ポート番号は整数で入力してください'
                    )
                    return
            
            # プロトコル
            protocol = self.protocol_combo.currentText()
            if protocol != '全て':
                self.conn_filter.add_protocol_filter([protocol])
            
            # 状態
            status = self.status_combo.currentText()
            if status != '全て':
                self.conn_filter.add_status_filter([status])
            
            self.refresh_data()
        
        def clear_filters(self):
            """フィルタをクリア"""
            self.process_input.clear()
            self.port_input.clear()
            self.protocol_combo.setCurrentIndex(0)
            self.status_combo.setCurrentIndex(0)
            self.conn_filter.clear()
            self.refresh_data()
        
        def toggle_auto_refresh(self):
            """自動更新の切り替え"""
            self.auto_refresh = not self.auto_refresh
            
            if self.auto_refresh:
                self.timer.start(3000)  # 3秒ごと
                self.auto_refresh_btn.setText('自動更新 停止')
                self.statusBar.showMessage('自動更新中（3秒間隔）')
            else:
                self.timer.stop()
                self.auto_refresh_btn.setText('自動更新 開始')
                self.statusBar.showMessage('自動更新を停止')
        
        def refresh_data(self):
            """データを更新"""
            try:
                # 接続情報を取得
                connections = self.monitor.get_connections()
                
                # フィルタ適用
                filtered = self.conn_filter.apply(connections)
                
                # テーブルを更新
                self.update_table(filtered)
                
                # 接続数を更新
                self.count_label.setText(f'接続数: {len(filtered)}')
                
                if not self.auto_refresh:
                    self.statusBar.showMessage('更新完了')
                
            except PermissionError:
                QMessageBox.critical(
                    self, 'エラー',
                    '管理者権限が必要です。\n管理者として実行してください。'
                )
            except Exception as e:
                QMessageBox.critical(
                    self, 'エラー',
                    f'データ取得中にエラーが発生しました:\n{str(e)}'
                )
        
        def update_table(self, connections):
            """テーブルを更新"""
            self.table.setRowCount(len(connections))
            
            for i, conn in enumerate(connections):
                self.table.setItem(i, 0, QTableWidgetItem(conn.process_name))
                self.table.setItem(i, 1, QTableWidgetItem(str(conn.pid)))
                self.table.setItem(i, 2, QTableWidgetItem(conn.local_address))
                self.table.setItem(i, 3, QTableWidgetItem(conn.remote_address))
                self.table.setItem(i, 4, QTableWidgetItem(conn.protocol))
                self.table.setItem(i, 5, QTableWidgetItem(conn.status))


def main():
    """GUIアプリケーションを起動"""
    if not PYQT_AVAILABLE:
        print("\nGUI版を使用するには PyQt6 をインストールしてください:")
        print("  pip install PyQt6")
        sys.exit(1)
    
    app = QApplication(sys.argv)
    window = NetworkMonitorGUI()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
