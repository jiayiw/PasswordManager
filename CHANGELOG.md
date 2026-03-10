# 更新日志 / Changelog

所有重要的更改都将记录在此文件中。

All notable changes to this project will be documented in this file.

---

## [1.0.0] - 2026-03-10

### 新增功能 / Added

#### 中文
- AES-256-GCM 加密存储密码数据
- 主密码保护（主密码不存储在任何地方）
- 密码管理功能（添加、编辑、删除、查看）
- 按网站名称搜索密码
- 一键复制密码到剪贴板，30秒后自动清除
- 随机密码生成器（16位，包含字母、数字、符号）
- 加密备份文件导出功能
- 加密备份文件导入功能
- 全角字符自动转换为半角字符
- PyQt6 现代化 GUI 界面
- macOS .app 应用包支持
- 跨平台支持（macOS、Linux）

#### English
- AES-256-GCM encryption for password storage
- Master password protection (master password is never stored)
- Password management (add, edit, delete, view)
- Search passwords by website name
- One-click copy password to clipboard with 30-second auto-clear
- Random password generator (16 characters with letters, numbers, symbols)
- Encrypted backup file export
- Encrypted backup file import
- Automatic full-width to half-width character conversion
- Modern GUI with PyQt6
- macOS .app bundle support
- Cross-platform support (macOS, Linux)

### 技术细节 / Technical Details

#### 中文
- 使用 PBKDF2-SHA256 进行密钥派生（100,000次迭代）
- 使用 AES-256-GCM 进行数据加密
- 密码数据库存储在 `~/.password_manager/vault.enc`
- 支持 PyInstaller 打包为独立应用

#### English
- PBKDF2-SHA256 for key derivation (100,000 iterations)
- AES-256-GCM for data encryption
- Password database stored at `~/.password_manager/vault.enc`
- Support for PyInstaller packaging as standalone application

### 安全说明 / Security Notes

#### 中文
- 主密码不存储在任何地方，忘记后无法恢复
- 所有数据在本地加密存储，不上传到任何服务器
- 备份文件使用相同的主密码加密

#### English
- Master password is never stored and cannot be recovered if forgotten
- All data is encrypted and stored locally, never uploaded to any server
- Backup files are encrypted with the same master password

---

## 未来计划 / Future Plans

### 计划功能 / Planned Features

#### 中文
- 云端同步支持（可选）
- 密码强度检测
- 密码过期提醒
- 浏览器插件支持
- 双因素认证
- 密码历史记录

#### English
- Cloud sync support (optional)
- Password strength checker
- Password expiration reminders
- Browser extension support
- Two-factor authentication
- Password history

---

## 版本命名规则 / Version Naming Convention

遵循 [语义化版本](https://semver.org/lang/zh-CN/) 规范：

Following [Semantic Versioning](https://semver.org/):

- **主版本号（MAJOR）**: 不兼容的 API 更改
- **次版本号（MINOR）**: 向后兼容的功能新增
- **修订号（PATCH）**: 向后兼容的问题修正

- **MAJOR**: Incompatible API changes
- **MINOR**: Backwards-compatible new features
- **PATCH**: Backwards-compatible bug fixes