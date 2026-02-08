#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
VideoCut CLI - 视频英译中字幕生成器
"""

import argparse
import os
import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from video_subtitle_translator.audio_extractor import extract_audio
from video_subtitle_translator.transcriber import Transcriber
from video_subtitle_translator.translator import Translator
from video_subtitle_translator.subtitle_generator import generate_srt, generate_ass
from video_subtitle_translator.subtitle_parser import parse_srt
from video_subtitle_translator.config import TEMP_DIR, WHISPER_MODEL_SIZE


def process_video(
    video_path,
    output_path=None,
    subtitle_path=None,
    model_size=None,
    keep_srt=False,
    language="en",
):
    """
    处理视频的主函数

    Args:
        video_path: 输入视频路径
        output_path: 输出视频路径
        subtitle_path: 字幕文件路径（可选）
        model_size: Whisper模型大小
        keep_srt: 是否保留字幕文件
        language: 视频语言
    """
    video_path = Path(video_path)
    if not video_path.exists():
        print(f"❌ 错误：视频文件不存在: {video_path}")
        return False

    # 创建临时目录
    temp_dir = Path(TEMP_DIR)
    temp_dir.mkdir(exist_ok=True)
    video_name = video_path.stem
    model_size = model_size or WHISPER_MODEL_SIZE

    try:
        # 步骤1-2: 语音识别或读取字幕
        if subtitle_path:
            print("=" * 60)
            print("步骤 1/3: 读取英文字幕文件...")
            print("=" * 60)
            segments = parse_srt(subtitle_path)
            if not segments:
                print(f"❌ 警告：无法解析字幕文件: {subtitle_path}")
                return False
            print(f"✓ 成功读取 {len(segments)} 个字幕片段")
            audio_path = temp_dir / f"{video_name}_audio.wav"
        else:
            print("=" * 60)
            print("步骤 1/5: 提取音频...")
            print("=" * 60)
            audio_path = temp_dir / f"{video_name}_audio.wav"
            extract_audio(str(video_path), str(audio_path))

            print("\n" + "=" * 60)
            print("步骤 2/5: 语音识别（Whisper）...")
            print("=" * 60)
            transcriber = Transcriber(model_size=model_size)
            segments = transcriber.transcribe(str(audio_path), language=language)
            if not segments:
                print("❌ 警告：未识别到任何语音内容")
                return False

        # 步骤3: 翻译
        step_num = "2/3" if subtitle_path else "3/5"
        print("\n" + "=" * 60)
        print(f"步骤 {step_num}: 翻译中文字幕（Ollama）...")
        print("=" * 60)
        translator = Translator()
        segments = translator.translate_segments(segments)

        # 步骤4: 生成字幕文件
        step_num = "3/3" if subtitle_path else "4/5"
        print("\n" + "=" * 60)
        print(f"步骤 {step_num}: 生成字幕文件...")
        print("=" * 60)
        ass_path = temp_dir / f"{video_name}_bilingual.ass"
        srt_path = temp_dir / f"{video_name}_bilingual.srt"
        generate_ass(segments, str(ass_path))
        generate_srt(segments, str(srt_path))

        # 步骤5: 合成视频
        print("\n" + "=" * 60)
        print("烧录字幕到视频...")
        print("=" * 60)
        from video_subtitle_translator.video_merger_alt import merge_with_drawtext

        output_video = merge_with_drawtext(str(video_path), str(srt_path), output_path)

        # 清理临时文件
        if not keep_srt:
            print("\n清理临时文件...")
            if not subtitle_path and audio_path.exists():
                audio_path.unlink()
            if ass_path.exists():
                ass_path.unlink()
            if srt_path.exists():
                srt_path.unlink()
        else:
            print(f"\n保留的字幕文件:")
            print(f"  - ASS: {ass_path}")
            print(f"  - SRT: {srt_path}")

        print("\n" + "=" * 60)
        print("✓ 处理完成！")
        print("=" * 60)
        print(f"输出视频: {output_video}")
        return True

    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback

        traceback.print_exc()
        return False


def main():
    """CLI入口函数"""
    parser = argparse.ArgumentParser(
        prog="videocut",
        description="🎬 视频英译中字幕生成器 - 一键将英语视频转换为中文字幕视频",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  videocut "D:\\videos\\lecture.mp4"                    # 基础用法
  videocut "D:\\videos\\lecture.mp4" -o "output.mp4"   # 指定输出
  videocut "video.mp4" -s "english.srt"               # 使用已有字幕
  videocut "video.mp4" -m small                       # 使用small模型（更快）
  videocut "video.mp4" -k                             # 保留字幕文件

更多信息: https://github.com/xiaosen6/VedioCut
        """,
    )

    parser.add_argument("video", help="输入视频文件的绝对路径")
    parser.add_argument(
        "-o",
        "--output",
        default=None,
        help="输出视频文件路径（默认: 原视频名_translated.mp4）",
    )
    parser.add_argument(
        "-s",
        "--subtitle",
        default=None,
        help="英文字幕文件路径（SRT格式），提供则跳过语音识别",
    )
    parser.add_argument(
        "-m",
        "--model",
        default=WHISPER_MODEL_SIZE,
        choices=["tiny", "base", "small", "medium", "large"],
        help=f"Whisper模型大小（默认: {WHISPER_MODEL_SIZE}）",
    )
    parser.add_argument(
        "-k", "--keep-srt", action="store_true", help="保留生成的字幕文件"
    )
    parser.add_argument(
        "-l", "--language", default="en", help="视频语言代码（默认: en）"
    )
    parser.add_argument("-v", "--version", action="version", version="%(prog)s 1.0.0")

    args = parser.parse_args()

    success = process_video(
        video_path=args.video,
        output_path=args.output,
        subtitle_path=args.subtitle,
        model_size=args.model,
        keep_srt=args.keep_srt,
        language=args.language,
    )

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
