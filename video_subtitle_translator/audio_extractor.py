"""
Audio extraction from video using ffmpeg
"""

import os
import subprocess
from pathlib import Path


def extract_audio(video_path: str, output_audio_path: str = None) -> str:
    """
    从视频中提取音频为WAV格式

    Args:
        video_path: 视频文件路径
        output_audio_path: 输出音频路径，默认生成临时文件

    Returns:
        音频文件路径
    """
    if output_audio_path is None:
        temp_dir = Path(__file__).parent.parent / "temp"
        temp_dir.mkdir(exist_ok=True)
        output_audio_path = temp_dir / "audio.wav"

    # ffmpeg命令：提取音频，16kHz采样率（whisper推荐），单声道
    cmd = [
        "ffmpeg",
        "-y",  # 覆盖已存在文件
        "-i",
        video_path,
        "-vn",  # 不处理视频
        "-acodec",
        "pcm_s16le",  # 16位PCM编码
        "-ar",
        "16000",  # 16kHz采样率
        "-ac",
        "1",  # 单声道
        str(output_audio_path),
    ]

    print(f"Extracting audio from: {video_path}")
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        raise RuntimeError(f"FFmpeg error: {result.stderr}")

    print(f"Audio extracted to: {output_audio_path}")
    return str(output_audio_path)
