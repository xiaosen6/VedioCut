"""
Video and subtitle merger using ffmpeg
"""

import os
import subprocess
from pathlib import Path
from typing import Optional


def merge_subtitle_to_video(
    video_path: str,
    subtitle_path: str,
    output_path: Optional[str] = None,
    subtitle_format: str = "ass",
) -> str:
    """
    将字幕烧录到视频中

    Args:
        video_path: 输入视频路径
        subtitle_path: 字幕文件路径（.srt或.ass）
        output_path: 输出视频路径，默认在原视频名后加 "_translated"
        subtitle_format: 字幕格式

    Returns:
        输出视频路径
    """
    video_path = Path(video_path)

    if output_path is None:
        # 默认输出路径：原视频名_translated.扩展名
        stem = video_path.stem
        suffix = video_path.suffix
        output_path = video_path.parent / f"{stem}_translated{suffix}"
    else:
        output_path = Path(output_path)

    subtitle_path = Path(subtitle_path)

    if not subtitle_path.exists():
        raise FileNotFoundError(f"Subtitle file not found: {subtitle_path}")

    print(f"Merging subtitle into video...")
    print(f"Input: {video_path}")
    print(f"Subtitle: {subtitle_path}")
    print(f"Output: {output_path}")

    # 构建ffmpeg命令
    # 使用字幕的绝对路径，Windows格式
    subtitle_abs = str(subtitle_path)

    # 使用subtitles滤镜处理字幕，直接指定绝对路径
    # 注意：Windows路径需要转义冒号和反斜杠
    vf_filter = f"subtitles='{subtitle_abs}'"

    cmd = [
        "ffmpeg",
        "-y",  # 覆盖已存在文件
        "-i",
        str(video_path),
        "-vf",
        vf_filter,
        "-c:a",
        "copy",  # 复制音频流，不重新编码
        "-c:v",
        "libx264",  # 视频编码器
        "-preset",
        "medium",  # 编码速度与质量平衡
        "-crf",
        "18",  # 视频质量（数值越小质量越高，18-23是视觉无损范围）
        str(output_path),
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        raise RuntimeError(f"FFmpeg error: {result.stderr}")

    print(f"Video with subtitle saved to: {output_path}")

    return str(output_path)


def burn_srt_with_style(
    video_path: str, srt_path: str, output_path: Optional[str] = None
) -> str:
    """
    使用FFmpeg的subtitles滤镜烧录SRT字幕（带样式）

    Args:
        video_path: 输入视频路径
        srt_path: SRT字幕路径
        output_path: 输出视频路径

    Returns:
        输出视频路径
    """
    video_path = Path(video_path)

    if output_path is None:
        stem = video_path.stem
        suffix = video_path.suffix
        output_path = video_path.parent / f"{stem}_translated{suffix}"
    else:
        output_path = Path(output_path)

    srt_path = Path(srt_path)

    # Windows路径处理
    srt_path_str = str(srt_path).replace("\\", "/")

    # 使用force_style参数设置字幕样式
    # FontName=Source Han Sans CN 需要系统中安装此字体
    style_params = (
        "FontName=Source Han Sans CN,"
        "FontSize=24,"
        "PrimaryColour=&H00FFFFFF,"  # 白色
        "OutlineColour=&H00000000,"  # 黑色描边
        "BackColour=&H80000000,"  # 半透明黑色背景
        "Bold=1,"
        "Outline=2,"
        "Shadow=0,"
        "Alignment=2,"  # 底部居中
        "MarginV=30"
    )

    cmd = [
        "ffmpeg",
        "-y",
        "-i",
        str(video_path),
        "-vf",
        f"subtitles={srt_path_str}:force_style='{style_params}'",
        "-c:a",
        "copy",
        "-c:v",
        "libx264",
        "-preset",
        "medium",
        "-crf",
        "18",
        str(output_path),
    ]

    print(f"Burning subtitle with style...")
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        raise RuntimeError(f"FFmpeg error: {result.stderr}")

    print(f"Video saved to: {output_path}")
    return str(output_path)
