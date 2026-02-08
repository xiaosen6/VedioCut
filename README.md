# VideoCut
🎬 视频英译中字幕生成器 - 一键将英语视频转换为中文字幕视频

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![CLI](https://img.shields.io/badge/CLI-Supported-brightgreen.svg)](CLI_INSTALL.md)

一个基于本地AI模型的视频字幕翻译工具，使用 OpenAI Whisper 进行语音识别，Ollama 进行翻译，FFmpeg 进行视频合成。

**🚀 最新特性：现已支持 CLI 命令行工具，安装后可在任何目录直接使用 `videocut` 命令！**

## ✨ 特性

- 🔊 **自动语音识别** - 使用 Whisper 模型自动提取英文字幕
- 🌐 **AI智能翻译** - 基于 Ollama 本地大模型逐句翻译
- 📝 **单语字幕输出** - 仅显示中文翻译（覆盖原字幕）
- 🎨 **优美字幕样式** - 黑色半透明背景 + 白色文字
- ⚡ **支持已有字幕** - 可直接翻译现有 SRT 字幕文件
- 🖥️ **纯本地运行** - 无需联网（除首次下载模型）
- 🛠️ **CLI命令行工具** - 安装后可在任意目录快速调用

## 📸 效果展示

```
原视频：纯英文语音
    ↓
处理后：中文字幕（黑色半透明背景条，白色文字）
```

## 🛠️ 系统要求

- Windows 10/11 / Linux / macOS
- Python 3.8+
- FFmpeg（需添加到系统PATH）
- Ollama（本地运行）
- NVIDIA GPU（推荐，可选）
- 4GB+ 可用磁盘空间

## 🚀 快速开始

### 方式一：CLI命令行工具（推荐）

#### 1. 克隆仓库

```bash
git clone https://github.com/xiaosen6/VedioCut.git
cd VedioCut
```

#### 2. 安装依赖

```bash
pip install -r requirements.txt
```

#### 3. 安装Ollama和翻译模型

1. 下载安装 [Ollama](https://ollama.com/)
2. 拉取翻译模型：
```bash
ollama pull translategemma:4b
```

#### 4. 安装CLI工具

**Windows:**
```cmd
install.bat
```
然后**重新打开**命令行窗口

**Linux/macOS:**
```bash
chmod +x install.sh
./install.sh
```

#### 5. 使用CLI命令

现在可以在任意目录使用：

```bash
# 基础用法
videocut "D:\videos\lecture.mp4"

# 指定输出文件名
videocut "input.mp4" -o "output_cn.mp4"

# 使用已有英文字幕（跳过语音识别，更快）
videocut "video.mp4" -s "english.srt"

# 保留生成的字幕文件
videocut "video.mp4" -k

# 使用更快的模型
videocut "video.mp4" -m small
```

### 方式二：Python脚本运行

如果不希望安装CLI，也可以直接使用Python运行：

```bash
python main.py --video "your_video.mp4"
```

更多参数见下方详细说明。

## 📖 CLI详细参数

### 命令格式

```bash
videocut <视频路径> [选项]
```

### 参数说明

| 参数 | 简写 | 说明 | 默认值 |
|------|------|------|--------|
| `video` | - | 输入视频文件的绝对路径（必需） | - |
| `--output` | `-o` | 输出视频文件路径 | 原视频名_translated |
| `--subtitle` | `-s` | 英文字幕文件路径（SRT格式），提供则跳过语音识别 | None |
| `--model` | `-m` | Whisper模型大小 | medium |
| `--keep-srt` | `-k` | 保留生成的字幕文件 | False |
| `--language` | `-l` | 视频语言代码 | en |
| `--version` | `-v` | 显示版本号 | - |
| `--help` | `-h` | 显示帮助信息 | - |

### 使用示例

```bash
# 1. 基础翻译
videocut "D:\videos\lecture.mp4"

# 2. 指定输出位置和文件名
videocut "D:\videos\lecture.mp4" -o "D:\output\lecture_cn.mp4"

# 3. 使用已有英文字幕（跳过语音识别，节省大量时间）
videocut "D:\videos\lecture.mp4" -s "D:\videos\lecture.srt"

# 4. 使用更快的small模型（适合快速预览）
videocut "D:\videos\lecture.mp4" -m small

# 5. 保留生成的字幕文件（用于后期编辑）
videocut "D:\videos\lecture.mp4" -k

# 6. 组合使用
videocut "D:\videos\lecture.mp4" -o "output.mp4" -m small -k
```

## 🎯 模型大小选择

| 模型 | 大小 | 速度 | 精度 | 适用场景 |
|------|------|------|------|----------|
| tiny | 39MB | 最快 | 一般 | 快速测试 |
| base | 74MB | 快 | 较好 | 日常对话 |
| small | 244MB | 中等 | 好 | 快速处理 |
| **medium** | **769MB** | 中等 | **很好** | **默认推荐** |
| large | 1.5GB | 慢 | 最好 | 高精度需求 |

**建议：**
- 日常视频：使用默认 `medium`
- 快速预览：使用 `small`
- 高精度需求：使用 `large`

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

**处理102个片段的示例时间：**
- 提取音频：5秒
- 语音识别：30秒
- AI翻译：2-3分钟（取决于片段数量和模型速度）
- 视频合成：20-30秒

## 📂 项目结构

```
VedioCut/
├── models/                          # Whisper模型存储
│   └── faster-whisper-medium/       # 自动下载
├── video_subtitle_translator/       # 核心代码包
│   ├── cli.py                       # CLI入口（新增）
│   ├── config.py                    # 配置
│   ├── audio_extractor.py           # 音频提取
│   ├── transcriber.py               # 语音识别
│   ├── translator.py                # AI翻译
│   ├── subtitle_parser.py           # 字幕解析
│   ├── subtitle_generator.py        # 字幕生成
│   ├── video_merger.py              # 视频合成
│   └── video_merger_alt.py          # 备用合成方案
├── temp/                            # 临时文件
├── videocut.bat                     # Windows CLI启动脚本
├── videocut_runner.bat              # Windows直接运行脚本
├── install.bat                      # Windows安装脚本
├── install.sh                       # Linux/macOS安装脚本
├── setup.py                         # pip安装配置
├── main.py                          # Python脚本入口
├── requirements.txt                 # 依赖
├── CLI_INSTALL.md                   # CLI详细安装指南
└── README.md                        # 本文件
```

## ⚙️ 配置文件

编辑 `video_subtitle_translator/config.py` 自定义设置：

```python
# Whisper配置
WHISPER_MODEL_SIZE = "medium"      # 模型大小: tiny/base/small/medium/large
WHISPER_DEVICE = "cuda"            # cuda 或 cpu
WHISPER_COMPUTE_TYPE = "float16"   # float16 或 int8

# Ollama配置
OLLAMA_HOST = "http://localhost:11434"
OLLAMA_MODEL = "translategemma:4b"

# 字幕样式
SUBTITLE_STYLE = {
    "font_name": "Source Han Sans CN",  # 字体
    "font_size": 24,                     # 字号
    "primary_color": "&H00FFFFFF",       # 白色
    "back_color": "&H80000000",          # 半透明黑色背景
}
```

## 🐛 常见问题

### Q: 提示 'videocut' 不是内部或外部命令？

**解决方法：**
1. 确保已运行 `install.bat`（Windows）或 `./install.sh`（Linux/macOS）
2. **重新打开**命令行窗口（环境变量需要重启生效）
3. 或使用临时脚本：`videocut_runner.bat "video.mp4"`

### Q: FFmpeg 未找到？

确保 FFmpeg 已安装并添加到系统 PATH：
```bash
ffmpeg -version
```

Windows安装：
```bash
winget install ffmpeg
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

### Q: 中文字体显示为方框？

需要安装中文字体，推荐「思源黑体」(Source Han Sans CN) 或「微软雅黑」。

### Q: 如何处理带空格的路径？

Windows路径包含空格时，请用双引号包裹：
```bash
videocut "D:\My Videos\lecture.mp4"
```

## 📝 更新日志

### v1.1.0 (2025-02-06)
- ✨ **新增 CLI 命令行工具支持**
- 🛠️ 添加 `install.bat` 和 `install.sh` 安装脚本
- 📝 添加 `setup.py` 支持 pip 安装
- 📖 新增 `CLI_INSTALL.md` 详细安装指南
- 🐛 修复 Windows 路径处理和编码问题
- ✅ 优化翻译 Prompt，避免冗长输出

### v1.0.0 (2025-02-06)
- ✨ 初始版本发布
- 🎉 支持语音识别 + AI 翻译 + 字幕烧录完整流程
- 🔧 支持已有字幕文件直接翻译
- 🎨 优化字幕样式（单语显示，黑色半透明背景）

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

[MIT License](LICENSE)

---

⭐ 如果这个项目对你有帮助，请给个 Star 支持一下！

**相关链接：**
- [详细CLI安装指南](CLI_INSTALL.md)
- [问题反馈](https://github.com/xiaosen6/VedioCut/issues)
