from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QMessageBox,
    QHBoxLayout,
    QTextEdit,
    QCheckBox,
)
from PyQt6.QtCore import Qt
from models import PasswordEntry
from typing import Optional
import secrets
import string
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import fullwidth_to_halfwidth


class AddEditDialog(QDialog):
    def __init__(self, entry: Optional[PasswordEntry] = None, parent=None):
        super().__init__(parent)
        self.entry = entry
        self.result_entry = None
        self.init_ui()

    def init_ui(self):
        title = "编辑密码" if self.entry else "添加密码"
        self.setWindowTitle(title)
        self.setFixedSize(480, 420)
        self.setModal(True)

        layout = QVBoxLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(30, 25, 30, 25)

        title_label = QLabel(title)
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #333;")
        layout.addWidget(title_label)

        form_layout = QVBoxLayout()
        form_layout.setSpacing(8)

        site_label = QLabel("网站名称:")
        site_label.setStyleSheet("font-size: 13px; color: #555;")
        form_layout.addWidget(site_label)

        self.site_input = QLineEdit()
        self.site_input.setPlaceholderText("例如: GitHub")
        self.site_input.setFixedHeight(40)
        form_layout.addWidget(self.site_input)

        username_label = QLabel("用户名:")
        username_label.setStyleSheet("font-size: 13px; color: #555;")
        form_layout.addWidget(username_label)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("用户名或邮箱")
        self.username_input.setFixedHeight(40)
        form_layout.addWidget(self.username_input)

        password_label = QLabel("密码:")
        password_label.setStyleSheet("font-size: 13px; color: #555;")
        form_layout.addWidget(password_label)

        password_row = QHBoxLayout()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setPlaceholderText("密码")
        self.password_input.setFixedHeight(40)
        password_row.addWidget(self.password_input, 1)

        self.show_password_cb = QCheckBox("显示")
        self.show_password_cb.setStyleSheet("font-size: 13px; color: #555;")
        self.show_password_cb.stateChanged.connect(self.toggle_password)
        password_row.addWidget(self.show_password_cb)

        self.gen_btn = QPushButton("生成")
        self.gen_btn.setFixedSize(60, 40)
        self.gen_btn.setStyleSheet("""
            QPushButton {
                background-color: #6c757d;
                color: white;
                border: none;
                border-radius: 6px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #5a6268;
            }
        """)
        self.gen_btn.clicked.connect(self.generate_password)
        password_row.addWidget(self.gen_btn)

        form_layout.addLayout(password_row)

        notes_label = QLabel("备注:")
        notes_label.setStyleSheet("font-size: 13px; color: #555;")
        form_layout.addWidget(notes_label)

        self.notes_input = QTextEdit()
        self.notes_input.setPlaceholderText("可选备注信息")
        self.notes_input.setFixedHeight(80)
        form_layout.addWidget(self.notes_input)

        layout.addLayout(form_layout)

        layout.addSpacing(10)

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        self.save_btn = QPushButton("保存")
        self.save_btn.setFixedSize(110, 40)
        self.save_btn.setStyleSheet("""
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
        self.save_btn.clicked.connect(self.save)
        btn_layout.addWidget(self.save_btn)

        btn_layout.addSpacing(15)

        self.cancel_btn = QPushButton("取消")
        self.cancel_btn.setFixedSize(110, 40)
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

        if self.entry:
            self.site_input.setText(self.entry.site)
            self.username_input.setText(self.entry.username)
            self.password_input.setText(self.entry.password)
            self.notes_input.setPlainText(self.entry.notes)

        self.setLayout(layout)
        self.site_input.setFocus()

    def toggle_password(self, state):
        if state == Qt.CheckState.Checked.value:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

    def generate_password(self):
        alphabet = string.ascii_letters + string.digits + string.punctuation
        password = "".join(secrets.choice(alphabet) for _ in range(16))
        self.password_input.setText(password)

    def save(self):
        site = fullwidth_to_halfwidth(self.site_input.text().strip())
        username = fullwidth_to_halfwidth(self.username_input.text().strip())
        password = fullwidth_to_halfwidth(self.password_input.text())
        notes = self.notes_input.toPlainText().strip()

        if not site:
            QMessageBox.warning(self, "错误", "请输入网站名称")
            return
        if not username:
            QMessageBox.warning(self, "错误", "请输入用户名")
            return
        if not password:
            QMessageBox.warning(self, "错误", "请输入密码")
            return

        if self.entry:
            self.entry.site = site
            self.entry.username = username
            self.entry.password = password
            self.entry.notes = notes
            self.result_entry = self.entry
        else:
            self.result_entry = PasswordEntry.create(site, username, password, notes)

        self.accept()
