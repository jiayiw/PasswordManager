from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QMessageBox,
    QHBoxLayout,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import fullwidth_to_halfwidth


class LoginDialog(QDialog):
    def __init__(self, is_new_vault: bool = False, parent=None):
        super().__init__(parent)
        self.is_new_vault = is_new_vault
        self.password = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("密码管理器 - 登录")
        window_height = 350 if self.is_new_vault else 280
        self.setFixedSize(450, window_height)
        self.setModal(True)

        layout = QVBoxLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(40, 30, 40, 30)

        title = QLabel("密码管理器")
        title.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: #333; margin-bottom: 10px;")
        layout.addWidget(title)

        if self.is_new_vault:
            hint = QLabel("首次使用，请设置主密码")
            hint.setAlignment(Qt.AlignmentFlag.AlignCenter)
            hint.setStyleSheet("color: #666; font-size: 13px; margin-bottom: 10px;")
            layout.addWidget(hint)

        self.password_label = QLabel("主密码:")
        self.password_label.setStyleSheet("font-size: 14px; color: #333;")
        layout.addWidget(self.password_label)

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setPlaceholderText("请输入主密码")
        self.password_input.setFixedHeight(42)
        self.password_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid #ccc;
                border-radius: 6px;
                padding: 8px 12px;
                font-size: 14px;
                background-color: #fff;
                color: #333;
            }
            QLineEdit:focus {
                border-color: #0078d4;
            }
            QLineEdit::placeholder {
                color: #999;
            }
        """)
        self.password_input.returnPressed.connect(self.login)
        layout.addWidget(self.password_input)

        if self.is_new_vault:
            self.confirm_label = QLabel("确认密码:")
            self.confirm_label.setStyleSheet("font-size: 14px; color: #333;")
            layout.addWidget(self.confirm_label)

            self.confirm_input = QLineEdit()
            self.confirm_input.setEchoMode(QLineEdit.EchoMode.Password)
            self.confirm_input.setPlaceholderText("请再次输入主密码")
            self.confirm_input.setFixedHeight(42)
            self.confirm_input.setStyleSheet("""
                QLineEdit {
                    border: 1px solid #ccc;
                    border-radius: 6px;
                    padding: 8px 12px;
                    font-size: 14px;
                    background-color: #fff;
                    color: #333;
                }
                QLineEdit:focus {
                    border-color: #0078d4;
                }
                QLineEdit::placeholder {
                    color: #999;
                }
            """)
            self.confirm_input.returnPressed.connect(self.login)
            layout.addWidget(self.confirm_input)

        layout.addSpacing(15)

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        self.login_btn = QPushButton("确定")
        self.login_btn.setFixedSize(120, 40)
        self.login_btn.setStyleSheet("""
            QPushButton {
                background-color: #0078d4;
                color: white;
                border: none;
                border-radius: 6px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #106ebe;
            }
            QPushButton:pressed {
                background-color: #005a9e;
            }
        """)
        self.login_btn.clicked.connect(self.login)
        btn_layout.addWidget(self.login_btn)

        btn_layout.addSpacing(15)

        self.cancel_btn = QPushButton("退出")
        self.cancel_btn.setFixedSize(120, 40)
        self.cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #f0f0f0;
                color: #333;
                border: 1px solid #ccc;
                border-radius: 6px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
            QPushButton:pressed {
                background-color: #d0d0d0;
            }
        """)
        self.cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(self.cancel_btn)

        btn_layout.addStretch()
        layout.addLayout(btn_layout)

        self.setLayout(layout)
        self.password_input.setFocus()

    def login(self):
        password = fullwidth_to_halfwidth(self.password_input.text())

        if not password:
            QMessageBox.warning(self, "错误", "请输入主密码")
            return

        if len(password) < 6:
            QMessageBox.warning(self, "错误", "密码长度至少6位")
            return

        if self.is_new_vault:
            confirm = fullwidth_to_halfwidth(self.confirm_input.text())
            if password != confirm:
                QMessageBox.warning(self, "错误", "两次输入的密码不一致")
                return

        self.password = password
        self.accept()
