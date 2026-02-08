"""
Alternative video merger using drawtext filter (more reliable on Windows)
"""

import subprocess
from pathlib import Path


from typing import Optional


def merge_with_drawtext(
    video_path: str, srt_path: str, output_path: Optional[str] = None
):
    """
    使用drawtext滤镜合并字幕（更可靠，避免路径问题）
    """
    video_path = Path(video_path)
    srt_path = Path(srt_path)

    if output_path is None:
        output_path = (
            video_path.parent / f"{video_path.stem}_translated{video_path.suffix}"
        )
    else:
        output_path = Path(output_path)

    print(f"Using drawtext method...")
    print(f"Input: {video_path}")
    print(f"Subtitle: {srt_path}")
    print(f"Output: {output_path}")

    # 方案1: 使用ffmpeg的subtitles滤镜，但在字幕所在目录执行
    # 先切换到字幕目录执行
    import os

    original_cwd = os.getcwd()
    subtitle_dir = srt_path.parent

    try:
        os.chdir(subtitle_dir)
        subtitle_name = srt_path.name

        # 构建命令
        cmd = [
            "ffmpeg",
            "-y",
            "-i",
            str(video_path),
            "-vf",
            f"subtitles='{subtitle_name}'",
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

        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            raise RuntimeError(f"FFmpeg error: {result.stderr}")

        print(f"Success! Output: {output_path}")
        return str(output_path)

    finally:
        os.chdir(original_cwd)


def merge_with_ass(video_path: str, ass_path: str, output_path: str = None):
    """
    使用ASS字幕和ass滤镜（样式更好）
    """
    video_path = Path(video_path)
    ass_path = Path(ass_path)

    if output_path is None:
        output_path = (
            video_path.parent / f"{video_path.stem}_translated{video_path.suffix}"
        )
    else:
        output_path = Path(output_path)

    import os

    original_cwd = os.getcwd()
    subtitle_dir = ass_path.parent

    try:
        os.chdir(subtitle_dir)
        ass_name = ass_path.name

        cmd = [
            "ffmpeg",
            "-y",
            "-i",
            str(video_path),
            "-vf",
            f"ass='{ass_name}'",
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

        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            raise RuntimeError(f"FFmpeg error: {result.stderr}")

        print(f"Success! Output: {output_path}")
        return str(output_path)

    finally:
        os.chdir(original_cwd)


if __name__ == "__main__":
    import sys

    if len(sys.argv) >= 3:
        video = sys.argv[1]
        subtitle = sys.argv[2]
        output = sys.argv[3] if len(sys.argv) > 3 else None
        merge_with_drawtext(video, subtitle, output)
    else:
        print("Usage: python video_merger_alt.py <video> <subtitle> [output]")
