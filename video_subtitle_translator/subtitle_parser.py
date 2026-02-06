"""
Subtitle parser for reading SRT files
"""

import re
from pathlib import Path
from typing import List, Dict


def parse_srt(srt_path: str) -> List[Dict]:
    """
    解析SRT字幕文件

    Args:
        srt_path: SRT文件路径

    Returns:
        字幕片段列表，每个包含 start, end, text
    """
    srt_path = Path(srt_path)

    if not srt_path.exists():
        raise FileNotFoundError(f"字幕文件不存在: {srt_path}")

    with open(srt_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 分割字幕条目（按空行分割）
    entries = re.split(r"\n\s*\n", content.strip())

    segments = []

    for entry in entries:
        lines = entry.strip().split("\n")
        if len(lines) < 3:
            continue

        # 第一行是序号，第二行是时间，剩余是文本
        try:
            # 解析时间行
            time_line = lines[1]
            match = re.match(
                r"(\d+:\d+:\d+[,.]\d+)\s*-->\s*(\d+:\d+:\d+[,.]\d+)", time_line
            )
            if not match:
                continue

            start_str, end_str = match.groups()
            start = parse_time(start_str)
            end = parse_time(end_str)

            # 剩余行是文本
            text = " ".join(lines[2:]).strip()

            segments.append({"start": start, "end": end, "text": text})
        except Exception as e:
            print(f"警告：解析字幕条目失败: {e}")
            continue

    return segments


def parse_time(time_str: str) -> float:
    """
    将时间字符串转换为秒数

    Args:
        time_str: 时间字符串，格式为 "HH:MM:SS,mmm" 或 "HH:MM:SS.mmm"

    Returns:
        秒数（浮点数）
    """
    # 替换逗号为点
    time_str = time_str.replace(",", ".")

    parts = time_str.split(":")
    if len(parts) != 3:
        raise ValueError(f"无效的时间格式: {time_str}")

    hours = int(parts[0])
    minutes = int(parts[1])
    seconds = float(parts[2])

    return hours * 3600 + minutes * 60 + seconds
