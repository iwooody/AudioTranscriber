# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller打包配置
打包命令: pyinstaller AudioTranscriber.spec
"""

from PyInstaller.building.build_main import Analysis, PYZ, EXE, COLLECT
import sys
import os

block_cipher = None

# 项目根目录
base_dir = os.path.abspath('.')

a = Analysis(
    ['src/main.py'],
    pathex=[base_dir],
    binaries=[],
    datas=[
        # 包含模型目录（空目录也会包含）
        ('models', 'models'),
        # 包含资源文件
        ('resources', 'resources'),
    ],
    hiddenimports=[
        # PyTorch相关
        'torch',
        'torchaudio',
        # Whisper
        'whisper',
        'whisper.model',
        'whisper.tokenizer',
        # 音频处理
        'librosa',
        'soundfile',
        # 科学计算
        'numpy',
        'scipy',
        'sklearn',
        'sklearn.cluster',
        # NLP
        'jieba',
        'transformers',
        # 其他
        'python-docx',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # 排除不需要的模块减小体积
        'matplotlib',
        'PIL',
        'tkinter',
        'PyQt5',
        'PySide2',
        'PySide6',
    ],
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
    name='AudioTranscriber',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # 不显示控制台窗口
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    # 图标（如果有）
    # icon='resources/icon.ico',
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='AudioTranscriber'
)
