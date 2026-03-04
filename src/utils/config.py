# -*- coding: utf-8 -*-
"""
配置文件和常量
"""

import os
from pathlib import Path

# 应用信息
APP_NAME = "AudioTranscriber"
VERSION = "1.0.0"

# 路径配置
BASE_DIR = Path(__file__).parent.parent.parent
DATA_DIR = BASE_DIR / "data"
MODELS_DIR = BASE_DIR / "models"
RECORDINGS_DIR = DATA_DIR / "recordings"

# 确保目录存在
DATA_DIR.mkdir(exist_ok=True)
RECORDINGS_DIR.mkdir(exist_ok=True)
MODELS_DIR.mkdir(exist_ok=True)

# 数据库路径
DB_PATH = DATA_DIR / "transcriber.db"

# 模型配置
WHISPER_MODEL = "base"  # tiny, base, small, medium, large
SUPPORTED_LANGUAGES = {
    "zh": "中文",
    "en": "英文",
    "ja": "日文",
    "ko": "韩文",
    "fr": "法文",
    "de": "德文",
    "es": "西班牙文",
    "auto": "自动检测"
}

# 音频配置
SAMPLE_RATE = 16000
MAX_AUDIO_DURATION = 3 * 60 * 60  # 3小时（秒）
SUPPORTED_AUDIO_FORMATS = [
    "*.mp3", "*.wav", "*.m4a", "*.flac", "*.ogg", "*.aac", "*.wma"
]

# UI配置
WINDOW_MIN_WIDTH = 1200
WINDOW_MIN_HEIGHT = 800

# 颜色配置（用于说话人区分）
SPEAKER_COLORS = [
    "#FF6B6B", "#4ECDC4", "#45B7D1", "#FFA07A", "#98D8C8",
    "#F7DC6F", "#BB8FCE", "#85C1E2", "#F8B739", "#52BE80"
]
