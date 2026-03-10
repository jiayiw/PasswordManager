# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['src/main.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['PyQt6.sip'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='PasswordManager',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='PasswordManager',
)

app = BUNDLE(
    coll,
    name='PasswordManager.app',
    icon=None,
    bundle_identifier='com.local.passwordmanager',
    info_plist={
        'CFBundleName': 'PasswordManager',
        'CFBundleDisplayName': '密码管理器',
        'CFBundleShortVersionString': '1.0',
        'CFBundleVersion': '1',
        'NSHighResolutionCapable': True,
        'LSMinimumSystemVersion': '10.13',
    },
)