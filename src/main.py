import sys
from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtCore import Qt
from gui.login_dialog import LoginDialog
from gui.main_window import MainWindow
import storage


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    app.setStyleSheet("""
        QMainWindow {
            background-color: #f5f5f5;
        }
        QLineEdit {
            border: 1px solid #ccc;
            border-radius: 6px;
            padding: 8px 12px;
            background-color: #fff;
            color: #333;
            font-size: 13px;
        }
        QLineEdit:focus {
            border-color: #0078d4;
        }
        QLineEdit::placeholder {
            color: #999;
        }
        QTextEdit {
            border: 1px solid #ccc;
            border-radius: 6px;
            padding: 8px;
            background-color: #fff;
            color: #333;
            font-size: 13px;
        }
        QTextEdit:focus {
            border-color: #0078d4;
        }
        QPushButton {
            padding: 8px 16px;
            border-radius: 6px;
            font-size: 13px;
        }
        QTableWidget {
            background-color: #fff;
            border: 1px solid #ddd;
            border-radius: 6px;
            gridline-color: #eee;
            font-size: 13px;
        }
        QTableWidget::item {
            padding: 8px;
        }
        QTableWidget::item:selected {
            background-color: #e3f2fd;
            color: #333;
        }
        QHeaderView::section {
            background-color: #f8f8f8;
            padding: 10px;
            border: none;
            border-bottom: 1px solid #ddd;
            font-weight: bold;
            color: #333;
        }
        QScrollBar:vertical {
            border: none;
            background-color: #f0f0f0;
            width: 10px;
            border-radius: 5px;
        }
        QScrollBar::handle:vertical {
            background-color: #ccc;
            border-radius: 5px;
            min-height: 20px;
        }
        QScrollBar::handle:vertical:hover {
            background-color: #bbb;
        }
    """)

    is_new_vault = not storage.vault_exists()

    login_dialog = LoginDialog(is_new_vault=is_new_vault)

    while True:
        if login_dialog.exec() != LoginDialog.DialogCode.Accepted:
            sys.exit(0)

        password = login_dialog.password

        if is_new_vault:
            vault = storage.create_vault(password)
            break
        else:
            vault = storage.load_vault(password)
            if vault is not None:
                break
            QMessageBox.warning(None, "错误", "主密码错误，请重试")
            login_dialog.password_input.clear()
            login_dialog.password_input.setFocus()

    window = MainWindow(vault, password)
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
