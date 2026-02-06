"""
Subtitle file generation (.srt format)
"""

from pathlib import Path
from typing import List, Dict
import re


def format_time(seconds: float) -> str:
    """将秒数格式化为SRT时间格式 HH:MM:SS,mmm"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"


def generate_srt(segments: List[Dict], output_path: str) -> str:
    """
    生成SRT字幕文件（双语）

    Args:
        segments: 转录结果列表（已翻译）
        output_path: 输出文件路径

    Returns:
        生成的字幕文件路径
    """
    print(f"Generating SRT file: {output_path}")

    with open(output_path, "w", encoding="utf-8") as f:
        for i, segment in enumerate(segments, 1):
            start_time = format_time(segment["start"])
            end_time = format_time(segment["end"])

            # 获取翻译（只显示中文）
            translated_text = segment.get("translation", "").strip()

            # 清理文本中的换行符
            translated_text = re.sub(r"\s+", " ", translated_text)

            # SRT格式：序号、时间轴、文本行（只显示中文）
            f.write(f"{i}\n")
            f.write(f"{start_time} --> {end_time}\n")
            f.write(f"{translated_text}\n")  # 只显示中文
            f.write("\n")

    print(f"SRT file generated: {output_path}")
    return output_path


def generate_ass(
    segments: List[Dict], output_path: str, style_config: dict = None
) -> str:
    """
    生成ASS字幕文件（支持更丰富的样式）

    Args:
        segments: 转录结果列表
        output_path: 输出文件路径
        style_config: 样式配置

    Returns:
        生成的字幕文件路径
    """
    print(f"Generating ASS file: {output_path}")

    # 默认样式
    default_style = {
        "font_name": "Source Han Sans CN",
        "font_size": 24,
        "primary_color": "&H00FFFFFF",  # 白色
        "secondary_color": "&H00FFFFFF",
        "outline_color": "&H00000000",
        "back_color": "&H80000000",  # 半透明黑色
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

    style = style_config or default_style

    # ASS头部
    ass_header = f"""[Script Info]
Title: Bilingual Subtitles
ScriptType: v4.00+
WrapStyle: 0
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,{style["font_name"]},{style["font_size"]},{style["primary_color"]},{style["secondary_color"]},{style["outline_color"]},{style["back_color"]},{style["bold"]},{style["italic"]},0,0,100,100,0,0,{style["border_style"]},{style["outline"]},{style["shadow"]},{style["alignment"]},{style["margin_l"]},{style["margin_r"]},{style["margin_v"]},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

    def format_ass_time(seconds: float) -> str:
        """ASS时间格式: H:MM:SS.cc"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        centis = int((seconds % 1) * 100)
        return f"{hours}:{minutes:02d}:{secs:02d}.{centis:02d}"

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(ass_header)

        for segment in segments:
            start_time = format_ass_time(segment["start"])
            end_time = format_ass_time(segment["end"])

            translated_text = segment.get("translation", "").strip()

            # 清理和转义
            translated_text = re.sub(r"\s+", " ", translated_text)

            # 单语字幕：只显示中文
            text = translated_text.replace("{", "\\{").replace("}", "\\}")

            f.write(f"Dialogue: 0,{start_time},{end_time},Default,,0,0,0,,{text}\n")

    print(f"ASS file generated: {output_path}")
    return output_path
