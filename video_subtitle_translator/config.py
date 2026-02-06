"""
Video Subtitle Translator Configuration
"""

import os

# 修复Windows上的OpenMP库冲突
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

# 项目根目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 模型存储目录
MODELS_DIR = os.path.join(BASE_DIR, "models")

# Whisper模型配置
WHISPER_MODEL_SIZE = "medium"  # tiny, base, small, medium, large
WHISPER_DEVICE = "cuda"  # 如果有NVIDIA GPU用"cuda"，否则用"cpu"
WHISPER_COMPUTE_TYPE = "float16"  # float16或int8

# Ollama配置
OLLAMA_HOST = "http://localhost:11434"
OLLAMA_MODEL = "translategemma:4b"

# 字幕样式配置
SUBTITLE_STYLE = {
    "font_name": "Source Han Sans CN",  # 思源黑体
    "font_size": 24,
    "primary_color": "&H00FFFFFF",  # 白色
    "secondary_color": "&H00FFFFFF",
    "outline_color": "&H00000000",  # 黑色描边
    "back_color": "&H80000000",  # 半透明黑色背景
    "bold": 1,
    "italic": 0,
    "border_style": 4,  # 背景框
    "outline": 1,
    "shadow": 0,
    "alignment": 2,  # 底部居中
    "margin_l": 10,
    "margin_r": 10,
    "margin_v": 30,
}

# 临时文件目录
TEMP_DIR = os.path.join(BASE_DIR, "temp")
os.makedirs(TEMP_DIR, exist_ok=True)
