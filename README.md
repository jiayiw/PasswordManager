# 密码管理器 / Password Manager

[中文](#中文) | [English](#english)

---

<a name="中文"></a>

## 中文

### 项目简介

一个简单、安全的本地密码管理器，使用 AES-256-GCM 加密算法保护您的密码数据。支持跨平台运行于 macOS 和 Linux 系统。

### 功能特性

- **AES-256-GCM 加密** - 使用工业级加密算法保护数据
- **主密码保护** - 所有数据通过主密码加密，主密码不存储在任何地方
- **密码管理** - 支持网站密码的增删改查操作
- **搜索功能** - 按网站名称快速搜索密码
- **一键复制** - 复制密码到剪贴板，30秒后自动清除
- **随机密码生成** - 生成16位强密码（字母+数字+符号）
- **备份与恢复** - 支持加密备份文件的导出和导入
- **全角字符转换** - 自动将全角字符转换为半角字符
- **跨平台支持** - 支持 macOS 和 Linux

### 安全说明

- **加密算法**: AES-256-GCM
- **密钥派生**: PBKDF2-SHA256（100,000次迭代）
- **主密码**: 不存储在任何地方，仅存在于用户记忆中
- **数据存储**: 加密后存储在本地文件 `~/.password_manager/vault.enc`

⚠️ **重要提示**：
- 请牢记主密码，忘记后无法恢复密码数据
- 请妥善保管备份文件，备份文件使用相同的主密码加密
- 建议定期备份密码数据库

### 系统要求

- Python 3.9+
- macOS 10.13+ 或 Linux

### 安装与使用

#### 方式一：从源码运行

```bash
# 克隆项目
git clone <repository-url>
cd password_manager

# 安装依赖
pip install PyQt6 cryptography

# 运行程序
cd src
python3 main.py
```

#### 方式二：使用打包应用

```bash
# 安装打包工具
pip install pyinstaller

# 打包应用
cd password_manager
python3 -m PyInstaller build.spec --clean

# 运行打包后的应用
# macOS:
open dist/PasswordManager.app

# Linux:
./dist/PasswordManager/PasswordManager
```

### 使用说明

#### 首次使用

1. 启动程序后，设置主密码（至少6位）
2. 请牢记主密码，忘记后无法恢复

#### 添加密码

1. 点击「添加密码」按钮
2. 填写网站名称、用户名、密码
3. 可选择生成随机密码
4. 点击「保存」

#### 搜索密码

在搜索框输入网站名称，列表会实时过滤显示匹配结果

#### 复制密码

点击对应条目的「复制」按钮，密码将复制到剪贴板，30秒后自动清除

#### 备份与恢复

- **导出备份**: 菜单栏 → 文件 → 导出备份
- **导入备份**: 菜单栏 → 文件 → 导入备份（会覆盖当前数据）

### 数据存储

- 密码数据库位置: `~/.password_manager/vault.enc`
- 备份文件格式: `.enc` 加密文件

### 技术架构

#### 加密流程

```
用户主密码 → PBKDF2-SHA256 (100,000次迭代) → 256位密钥
                                              ↓
密码数据 → AES-256-GCM 加密 → 加密文件 (vault.enc)
```

#### 项目结构

```
password_manager/
├── src/
│   ├── main.py              # 程序入口
│   ├── crypto.py            # 加密模块
│   ├── models.py            # 数据模型
│   ├── storage.py           # 存储模块
│   ├── utils.py             # 工具函数
│   └── gui/
│       ├── login_dialog.py  # 登录窗口
│       ├── main_window.py   # 主窗口
│       └── add_dialog.py    # 添加/编辑对话框
├── build.spec               # PyInstaller 配置
├── requirements.txt         # 依赖列表
├── README.md
├── CHANGELOG.md
└── LICENSE
```

#### 依赖

- PyQt6 >= 6.4.0 - GUI 框架
- cryptography >= 41.0.0 - 加密库

### 开发指南

#### 环境配置

```bash
# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装开发依赖
pip install PyQt6 cryptography pyinstaller
```

#### 打包命令

```bash
# 清理并打包
python3 -m PyInstaller build.spec --clean

# 输出位置
# macOS: dist/PasswordManager.app
# Linux: dist/PasswordManager/
```

### 许可证

本项目采用 MIT 许可证，详见 [LICENSE](LICENSE) 文件。

---

<a name="english"></a>

## English

### Introduction

A simple and secure local password manager that uses AES-256-GCM encryption to protect your password data. Cross-platform support for macOS and Linux.

### Features

- **AES-256-GCM Encryption** - Industrial-grade encryption algorithm
- **Master Password Protection** - All data encrypted with master password, never stored anywhere
- **Password Management** - Add, edit, delete, and search passwords
- **Search Function** - Quick search by website name
- **One-Click Copy** - Copy password to clipboard, auto-clear after 30 seconds
- **Random Password Generator** - Generate 16-character strong passwords
- **Backup & Restore** - Export and import encrypted backup files
- **Full-width Character Conversion** - Auto-convert full-width to half-width characters
- **Cross-Platform** - Support for macOS and Linux

### Security

- **Encryption Algorithm**: AES-256-GCM
- **Key Derivation**: PBKDF2-SHA256 (100,000 iterations)
- **Master Password**: Never stored, exists only in user's memory
- **Data Storage**: Encrypted and stored locally at `~/.password_manager/vault.enc`

⚠️ **Important**:
- Remember your master password - it cannot be recovered if forgotten
- Keep your backup files safe - they are encrypted with the same master password
- Regular backups are recommended

### System Requirements

- Python 3.9+
- macOS 10.13+ or Linux

### Installation & Usage

#### Option 1: Run from Source

```bash
# Clone the repository
git clone <repository-url>
cd password_manager

# Install dependencies
pip install PyQt6 cryptography

# Run the application
cd src
python3 main.py
```

#### Option 2: Use Packaged Application

```bash
# Install packaging tool
pip install pyinstaller

# Build application
cd password_manager
python3 -m PyInstaller build.spec --clean

# Run the packaged application
# macOS:
open dist/PasswordManager.app

# Linux:
./dist/PasswordManager/PasswordManager
```

### Usage Guide

#### First Time Use

1. Launch the application and set a master password (minimum 6 characters)
2. Remember your master password - it cannot be recovered

#### Adding a Password

1. Click the "Add Password" button
2. Fill in website name, username, and password
3. Optionally generate a random password
4. Click "Save"

#### Searching Passwords

Type the website name in the search box, the list will filter results in real-time

#### Copying Passwords

Click the "Copy" button for the entry. The password will be copied to clipboard and auto-cleared after 30 seconds.

#### Backup & Restore

- **Export Backup**: Menu Bar → File → Export Backup
- **Import Backup**: Menu Bar → File → Import Backup (will overwrite current data)

### Data Storage

- Password database location: `~/.password_manager/vault.enc`
- Backup file format: `.enc` encrypted file

### Technical Architecture

#### Encryption Flow

```
Master Password → PBKDF2-SHA256 (100,000 iterations) → 256-bit Key
                                                          ↓
Password Data → AES-256-GCM Encryption → Encrypted File (vault.enc)
```

#### Project Structure

```
password_manager/
├── src/
│   ├── main.py              # Application entry
│   ├── crypto.py            # Encryption module
│   ├── models.py            # Data models
│   ├── storage.py           # Storage module
│   ├── utils.py             # Utility functions
│   └── gui/
│       ├── login_dialog.py  # Login dialog
│       ├── main_window.py   # Main window
│       └── add_dialog.py    # Add/Edit dialog
├── build.spec               # PyInstaller config
├── requirements.txt         # Dependencies
├── README.md
├── CHANGELOG.md
└── LICENSE
```

#### Dependencies

- PyQt6 >= 6.4.0 - GUI framework
- cryptography >= 41.0.0 - Encryption library

### Development Guide

#### Environment Setup

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install development dependencies
pip install PyQt6 cryptography pyinstaller
```

#### Build Commands

```bash
# Clean and build
python3 -m PyInstaller build.spec --clean

# Output location
# macOS: dist/PasswordManager.app
# Linux: dist/PasswordManager/
```

### License

This project is licensed under the MIT License. See [LICENSE](LICENSE) file for details.