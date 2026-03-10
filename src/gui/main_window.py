from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QMessageBox,
    QFileDialog,
    QApplication,
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QAction, QColor
from models import Vault, PasswordEntry
from gui.add_dialog import AddEditDialog
import storage


class MainWindow(QMainWindow):
    def __init__(self, vault: Vault, password: str):
        super().__init__()
        self.vault = vault
        self.password = password
        self.clipboard_timer = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("密码管理器")
        self.setMinimumSize(900, 650)

        self.init_menu()

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(20)

        search_layout = QHBoxLayout()
        search_layout.setSpacing(15)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 搜索网站名称...")
        self.search_input.setFixedHeight(42)
        self.search_input.textChanged.connect(self.search)
        search_layout.addWidget(self.search_input, 1)

        self.add_btn = QPushButton("添加密码")
        self.add_btn.setFixedSize(120, 42)
        self.add_btn.clicked.connect(self.add_entry)
        self.add_btn.setStyleSheet("""
            QPushButton {
                background-color: #0078d4;
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #106ebe;
            }
            QPushButton:pressed {
                background-color: #005a9e;
            }
        """)
        search_layout.addWidget(self.add_btn)

        layout.addLayout(search_layout)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["网站", "用户名", "备注", "操作"])
        self.table.horizontalHeader().setSectionResizeMode(
            0, QHeaderView.ResizeMode.Stretch
        )
        self.table.horizontalHeader().setSectionResizeMode(
            1, QHeaderView.ResizeMode.Stretch
        )
        self.table.horizontalHeader().setSectionResizeMode(
            2, QHeaderView.ResizeMode.Stretch
        )
        self.table.horizontalHeader().setSectionResizeMode(
            3, QHeaderView.ResizeMode.Fixed
        )
        self.table.setColumnWidth(3, 240)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setAlternatingRowColors(True)
        self.table.verticalHeader().setVisible(False)
        self.table.verticalHeader().setDefaultSectionSize(55)
        self.table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #ddd;
                border-radius: 8px;
                gridline-color: #eee;
                background-color: #fff;
                font-size: 13px;
                alternate-background-color: #f8f9fa;
            }
            QTableWidget::item {
                padding: 10px 8px;
                border-bottom: 1px solid #eee;
                color: #333;
            }
            QTableWidget::item:alternate {
                background-color: #f8f9fa;
                color: #333;
            }
            QTableWidget::item:selected {
                background-color: #e3f2fd;
                color: #333;
            }
            QTableWidget::item:hover {
                background-color: #f0f0f0;
            }
            QHeaderView::section {
                background-color: #f8f9fa;
                padding: 12px 8px;
                border: none;
                border-bottom: 2px solid #e0e0e0;
                font-weight: bold;
                color: #333;
                font-size: 13px;
            }
            QTableWidget QScrollBar:vertical {
                border: none;
                background-color: #f0f0f0;
                width: 10px;
                border-radius: 5px;
            }
            QTableWidget QScrollBar::handle:vertical {
                background-color: #ccc;
                border-radius: 5px;
                min-height: 20px;
            }
            QTableWidget QScrollBar::handle:vertical:hover {
                background-color: #bbb;
            }
        """)
        layout.addWidget(self.table)

        central_widget.setLayout(layout)

        self.refresh_table()

    def init_menu(self):
        menubar = self.menuBar()

        file_menu = menubar.addMenu("文件")

        export_action = QAction("导出备份", self)
        export_action.setShortcut("Ctrl+E")
        export_action.triggered.connect(self.export_vault)
        file_menu.addAction(export_action)

        import_action = QAction("导入备份", self)
        import_action.setShortcut("Ctrl+I")
        import_action.triggered.connect(self.import_vault)
        file_menu.addAction(import_action)

        file_menu.addSeparator()

        exit_action = QAction("退出", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

    def refresh_table(self, entries=None):
        if entries is None:
            entries = self.vault.entries

        self.table.setRowCount(len(entries))

        for row, entry in enumerate(entries):
            site_item = QTableWidgetItem(entry.site)
            site_item.setForeground(QColor("#333"))
            site_item.setTextAlignment(
                Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft
            )
            self.table.setItem(row, 0, site_item)

            username_item = QTableWidgetItem(entry.username)
            username_item.setForeground(QColor("#333"))
            username_item.setTextAlignment(
                Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft
            )
            self.table.setItem(row, 1, username_item)

            notes_item = QTableWidgetItem(entry.notes)
            notes_item.setForeground(QColor("#666"))
            notes_item.setTextAlignment(
                Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft
            )
            self.table.setItem(row, 2, notes_item)

            btn_widget = QWidget()
            btn_widget.setStyleSheet(
                "background: transparent; margin: 0px; padding: 0px;"
            )
            btn_layout = QHBoxLayout()
            btn_layout.setContentsMargins(10, 0, 10, 0)
            btn_layout.setSpacing(8)

            copy_btn = QPushButton("复制")
            copy_btn.setFixedSize(58, 34)
            copy_btn.clicked.connect(
                lambda checked, p=entry.password: self.copy_password(p)
            )
            copy_btn.setStyleSheet("""
                QPushButton {
                    background-color: #28a745;
                    color: white;
                    border: none;
                    border-radius: 5px;
                    font-size: 12px;
                    padding: 0px 4px;
                }
                QPushButton:hover {
                    background-color: #218838;
                }
                QPushButton:pressed {
                    background-color: #1e7e34;
                }
            """)
            btn_layout.addWidget(copy_btn)

            edit_btn = QPushButton("编辑")
            edit_btn.setFixedSize(58, 34)
            edit_btn.clicked.connect(lambda checked, e=entry: self.edit_entry(e))
            edit_btn.setStyleSheet("""
                QPushButton {
                    background-color: #ffc107;
                    color: #333;
                    border: none;
                    border-radius: 5px;
                    font-size: 12px;
                    padding: 0px 4px;
                }
                QPushButton:hover {
                    background-color: #e0a800;
                }
                QPushButton:pressed {
                    background-color: #d39e00;
                }
            """)
            btn_layout.addWidget(edit_btn)

            del_btn = QPushButton("删除")
            del_btn.setFixedSize(58, 34)
            del_btn.clicked.connect(lambda checked, e=entry: self.delete_entry(e))
            del_btn.setStyleSheet("""
                QPushButton {
                    background-color: #dc3545;
                    color: white;
                    border: none;
                    border-radius: 5px;
                    font-size: 12px;
                    padding: 0px 4px;
                }
                QPushButton:hover {
                    background-color: #c82333;
                }
                QPushButton:pressed {
                    background-color: #bd2130;
                }
            """)
            btn_layout.addWidget(del_btn)

            btn_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            btn_widget.setLayout(btn_layout)
            self.table.setCellWidget(row, 3, btn_widget)

    def search(self, text):
        entries = self.vault.search(text)
        self.refresh_table(entries)

    def add_entry(self):
        dialog = AddEditDialog(parent=self)
        if dialog.exec():
            if dialog.result_entry:
                self.vault.add_entry(dialog.result_entry)
                storage.save_vault(self.vault, self.password)
                self.refresh_table()

    def edit_entry(self, entry: PasswordEntry):
        dialog = AddEditDialog(entry=entry, parent=self)
        if dialog.exec():
            if dialog.result_entry:
                self.vault.update_entry(dialog.result_entry)
                storage.save_vault(self.vault, self.password)
                self.refresh_table()

    def delete_entry(self, entry: PasswordEntry):
        reply = QMessageBox.question(
            self,
            "确认删除",
            f'确定要删除 "{entry.site}" 的密码吗?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.vault.delete_entry(entry.id)
            storage.save_vault(self.vault, self.password)
            self.refresh_table()

    def copy_password(self, password: str):
        clipboard = QApplication.clipboard()
        clipboard.setText(password)

        if self.clipboard_timer:
            self.clipboard_timer.stop()

        self.clipboard_timer = QTimer()
        self.clipboard_timer.setSingleShot(True)
        self.clipboard_timer.timeout.connect(self.clear_clipboard)
        self.clipboard_timer.start(30000)

        QMessageBox.information(self, "已复制", "密码已复制到剪贴板，30秒后自动清除")

    def clear_clipboard(self):
        clipboard = QApplication.clipboard()
        clipboard.clear()

    def export_vault(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self, "导出备份", "vault_backup.enc", "加密文件 (*.enc)"
        )
        if file_path:
            try:
                storage.export_vault(self.vault, self.password, file_path)
                QMessageBox.information(self, "成功", "备份导出成功")
            except Exception as e:
                QMessageBox.critical(self, "错误", f"导出失败: {str(e)}")

    def import_vault(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "导入备份", "", "加密文件 (*.enc)"
        )
        if file_path:
            reply = QMessageBox.question(
                self,
                "确认导入",
                "导入将覆盖当前所有密码，确定继续吗?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            )
            if reply == QMessageBox.StandardButton.Yes:
                try:
                    imported = storage.import_vault(file_path, self.password)
                    if imported:
                        self.vault = imported
                        storage.save_vault(self.vault, self.password)
                        self.refresh_table()
                        QMessageBox.information(self, "成功", "备份导入成功")
                    else:
                        QMessageBox.critical(
                            self, "错误", "导入失败，密码错误或文件损坏"
                        )
                except Exception as e:
                    QMessageBox.critical(self, "错误", f"导入失败: {str(e)}")

    def closeEvent(self, event):
        if self.clipboard_timer:
            self.clipboard_timer.stop()
        event.accept()
