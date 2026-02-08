# VideoCut CLI 安装和使用指南

## 🚀 快速安装

### Windows 安装

1. **下载项目**
```bash
git clone https://github.com/xiaosen6/VedioCut.git
cd VedioCut
```

2. **一键安装（自动添加到环境变量）**
```bash
install.bat
```

3. **验证安装**
```bash
videocut --version
```

### Linux/macOS 安装

1. **下载项目**
```bash
git clone https://github.com/xiaosen6/VedioCut.git
cd VedioCut
```

2. **运行安装脚本**
```bash
chmod +x install.sh
./install.sh
```

3. **验证安装**
```bash
videocut --version
```

### 手动安装（高级用户）

如果不想使用安装脚本，可以手动安装：

#### 方法1: pip安装（推荐）
```bash
cd VedioCut
pip install -e .
```

这会安装 `videocut` 命令到系统PATH。

#### 方法2: 手动添加到PATH

**Windows:**
1. 复制项目路径（如 `D:\VedioCut`）
2. 右键"此电脑" → 属性 → 高级系统设置 → 环境变量
3. 编辑用户变量的 `Path`
4. 添加项目路径
5. 新建 `videocut.bat` 文件：
```batch
@echo off
python "D:\VedioCut\video_subtitle_translator\cli.py" %*
```

**Linux/macOS:**
```bash
# 创建符号链接
sudo ln -s $(pwd)/video_subtitle_translator/cli.py /usr/local/bin/videocut
chmod +x /usr/local/bin/videocut
```

## 🎬 使用方法

### 基础用法

```bash
# 处理视频（自动语音识别+翻译）
videocut "D:\videos\lecture.mp4"

# 指定输出文件名
videocut "D:\videos\lecture.mp4" -o "chinese_lecture.mp4"

# 使用已有英文字幕（跳过语音识别）
videocut "D:\videos\lecture.mp4" -s "D:\videos\lecture.srt"
```

### 高级选项

```bash
# 使用更快的模型（精度稍低）
videocut "video.mp4" -m small

# 保留生成的字幕文件
videocut "video.mp4" -k

# 指定语言（默认为英语）
videocut "video.mp4" -l en

# 组合使用
videocut "video.mp4" -o "output.mp4" -m small -k
```

### 完整参数列表

```
用法: videocut [选项] <视频路径>

位置参数:
  video                 输入视频文件的绝对路径

选项:
  -h, --help            显示帮助信息
  -o, --output          输出视频文件路径
  -s, --subtitle        英文字幕文件路径（跳过语音识别）
  -m, --model           Whisper模型: tiny/base/small/medium/large
  -k, --keep-srt        保留生成的字幕文件
  -l, --language        视频语言代码（默认: en）
  -v, --version         显示版本号
```

## 💡 使用技巧

### 1. 处理长视频
对于长视频，可以使用更快的模型：
```bash
videocut "long_video.mp4" -m small
```

### 2. 批量处理
创建批处理脚本：

**Windows (batch.bat):**
```batch
@echo off
for %%f in (*.mp4) do (
    videocut "%%f" -o "translated_%%f"
)
```

**Linux/macOS (batch.sh):**
```bash
for f in *.mp4; do
    videocut "$f" -o "translated_$f"
done
```

### 3. 处理特定目录
```bash
# Windows
videocut "%USERPROFILE%\Videos\lecture.mp4"

# Linux/macOS
videocut "$HOME/Videos/lecture.mp4"
```

## 🔧 环境要求

安装前请确保：

1. **Python 3.8+** 已安装
   ```bash
   python --version
   ```

2. **FFmpeg** 已安装并添加到PATH
   ```bash
   ffmpeg -version
   ```

3. **Ollama** 已安装并运行
   ```bash
   ollama --version
   ollama list  # 确保有 translategemma:4b
   ```

## 🐛 故障排除

### "videocut 不是内部或外部命令"

**Windows:**
1. 重新运行 `install.bat`
2. 重新打开命令提示符窗口
3. 或手动添加到PATH

**Linux/macOS:**
```bash
# 检查安装
which videocut

# 如果没有，手动添加
export PATH="$HOME/.local/bin:$PATH"
```

### 其他问题

查看主README.md的常见问题部分。

## 📚 更多信息

- 项目主页: https://github.com/xiaosen6/VedioCut
- 问题反馈: https://github.com/xiaosen6/VedioCut/issues
