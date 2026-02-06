# VideoCut
🎬 视频英译中字幕生成器 - 一键将英语视频转换为中文字幕视频

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

一个基于本地AI模型的视频字幕翻译工具，使用 OpenAI Whisper 进行语音识别，Ollama 进行翻译，FFmpeg 进行视频合成。

## ✨ 特性

- 🔊 **自动语音识别** - 使用 Whisper 模型自动提取英文字幕
- 🌐 **AI智能翻译** - 基于 Ollama 本地大模型逐句翻译
- 📝 **单语字幕输出** - 仅显示中文翻译（覆盖原字幕）
- 🎨 **优美字幕样式** - 黑色半透明背景 + 白色文字
- ⚡ **支持已有字幕** - 可直接翻译现有 SRT 字幕文件
- 🖥️ **纯本地运行** - 无需联网（除首次下载模型）

## 📸 效果展示

处理前 → 处理后

```
原视频：纯英文语音
处理后：中文字幕（黑色背景条）
```

## 🛠️ 系统要求

- Windows 10/11 / Linux / macOS
- Python 3.8+
- NVIDIA GPU（推荐，可选）
- 4GB+ 可用磁盘空间

## 🚀 快速开始

### 1. 克隆仓库

```bash
git clone https://github.com/xiaosen6/VedioCut.git
cd VedioCut
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

**确保已安装 FFmpeg 并添加到系统 PATH**

Windows 安装 FFmpeg:
```bash
winget install ffmpeg
```

### 3. 安装 Ollama 和翻译模型

1. 下载安装 [Ollama](https://ollama.com/)
2. 拉取翻译模型：
```bash
ollama pull translategemma:4b
```

### 4. 运行程序

**基础用法（自动识别+翻译）：**
```bash
python main.py --video "your_video.mp4"
```

**已有英文字幕（跳过识别）：**
```bash
python main.py --video "video.mp4" --subtitle "english.srt"
```

**指定输出文件名：**
```bash
python main.py --video "input.mp4" --output "output_cn.mp4"
```

**保留字幕文件：**
```bash
python main.py --video "video.mp4" --keep-srt
```

## 📖 详细参数

| 参数 | 简写 | 说明 | 默认值 |
|------|------|------|--------|
| `--video` | `-v` | 输入视频文件路径（必需） | - |
| `--output` | `-o` | 输出视频文件路径 | 原视频名_translated |
| `--subtitle` | `-s` | 英文字幕文件路径（SRT格式），提供则跳过语音识别 | None |
| `--model` | `-m` | Whisper模型大小 | medium |
| `--keep-srt` | `-k` | 保留生成的字幕文件 | False |
| `--language` | `-l` | 视频语言代码 | en |

### 模型大小选择

| 模型 | 大小 | 速度 | 精度 | 适用场景 |
|------|------|------|------|----------|
| tiny | 39MB | 最快 | 一般 | 快速测试 |
| base | 74MB | 快 | 较好 | 日常对话 |
| small | 244MB | 中等 | 好 | 推荐使用 |
| **medium** | **769MB** | 中等 | **很好** | **默认推荐** |
| large | 1.5GB | 慢 | 最好 | 高精度需求 |

## 🔧 工作流程

```
输入视频
    ↓
1. 提取音频 (ffmpeg)
    ↓
2. 语音识别 (Whisper) → 英文文本 + 时间轴
    ↓
3. AI翻译 (Ollama) → 中文文本
    ↓
4. 生成字幕 (SRT/ASS)
    ↓
5. 烧录字幕 (ffmpeg) → 输出视频
```

## ⚙️ 配置文件

编辑 `video_subtitle_translator/config.py` 自定义设置：

```python
# Whisper配置
WHISPER_MODEL_SIZE = "medium"      # 模型大小
WHISPER_DEVICE = "cuda"            # cuda 或 cpu
WHISPER_COMPUTE_TYPE = "float16"   # float16 或 int8

# Ollama配置
OLLAMA_HOST = "http://localhost:11434"
OLLAMA_MODEL = "translategemma:4b"

# 字幕样式
SUBTITLE_STYLE = {
    "font_name": "Source Han Sans CN",
    "font_size": 24,
    "primary_color": "&H00FFFFFF",      # 白色
    "back_color": "&H80000000",         # 半透明黑色背景
    ...
}
```

## 📂 项目结构

```
VedioCut/
├── models/                          # Whisper模型存储
│   └── faster-whisper-medium/
├── video_subtitle_translator/       # 核心代码包
│   ├── config.py                    # 配置
│   ├── audio_extractor.py           # 音频提取
│   ├── transcriber.py               # 语音识别
│   ├── translator.py                # 翻译
│   ├── subtitle_parser.py           # 字幕解析
│   ├── subtitle_generator.py        # 字幕生成
│   ├── video_merger.py              # 视频合成
│   └── video_merger_alt.py          # 备用合成方案
├── temp/                            # 临时文件
├── main.py                          # 主程序
├── requirements.txt                 # 依赖
└── README.md                        # 本文件
```

## 🐛 常见问题

### Q: FFmpeg 未找到？
确保 FFmpeg 已安装并添加到系统 PATH：
```bash
ffmpeg -version
```

### Q: Ollama 连接失败？
确保 Ollama 服务正在运行：
```bash
ollama serve
ollama list  # 查看已安装模型
```

### Q: CUDA 内存不足？
修改 `config.py` 使用 CPU：
```python
WHISPER_DEVICE = "cpu"
WHISPER_COMPUTE_TYPE = "int8"
```

### Q: 翻译结果太长？
已在 `translator.py` 中优化 Prompt，限制模型只输出简洁翻译。

### Q: 中文字体显示为方框？
需要安装中文字体，如「思源黑体」(Source Han Sans CN)。

## 📝 更新日志

### v1.0.0 (2025-02-06)
- ✨ 初始版本发布
- 🎉 支持语音识别 + AI 翻译 + 字幕烧录完整流程
- 🔧 支持已有字幕文件直接翻译
- 🎨 优化字幕样式（单语显示）

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

[MIT License](LICENSE)

---

⭐ 如果这个项目对你有帮助，请给个 Star 支持一下！
