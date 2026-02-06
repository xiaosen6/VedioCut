"""
Main entry point for Video Subtitle Translator
"""

import argparse
import os
import sys
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from video_subtitle_translator.audio_extractor import extract_audio
from video_subtitle_translator.transcriber import Transcriber
from video_subtitle_translator.translator import Translator
from video_subtitle_translator.subtitle_generator import generate_srt, generate_ass
from video_subtitle_translator.video_merger import merge_subtitle_to_video
from video_subtitle_translator.config import TEMP_DIR, WHISPER_MODEL_SIZE


def main():
    parser = argparse.ArgumentParser(
        description="视频英译中字幕生成器 - 提取英文字幕并翻译成中文后烧录到视频"
    )
    parser.add_argument("--video", "-v", required=True, help="输入视频文件路径")
    parser.add_argument(
        "--output",
        "-o",
        default=None,
        help="输出视频文件路径（可选，默认在原视频名后加 '_translated'）",
    )
    parser.add_argument(
        "--subtitle",
        "-s",
        default=None,
        help="英文字幕文件路径（SRT格式），提供则跳过语音识别",
    )
    parser.add_argument(
        "--model",
        "-m",
        default=WHISPER_MODEL_SIZE,
        choices=["tiny", "base", "small", "medium", "large"],
        help=f"Whisper模型大小（默认: {WHISPER_MODEL_SIZE}）",
    )
    parser.add_argument(
        "--keep-srt", "-k", action="store_true", help="保留生成的字幕文件"
    )
    parser.add_argument(
        "--language", "-l", default="en", help="视频语言代码（默认: en）"
    )

    args = parser.parse_args()

    # 验证输入视频存在
    video_path = Path(args.video)
    if not video_path.exists():
        print(f"错误：视频文件不存在: {video_path}")
        sys.exit(1)

    # 创建临时目录
    temp_dir = Path(TEMP_DIR)
    temp_dir.mkdir(exist_ok=True)

    # 视频基础名（用于临时文件）
    video_name = video_path.stem

    try:
        # 检查是否提供了字幕文件
        if args.subtitle:
            # 步骤1-2: 直接读取提供的字幕文件
            print("=" * 60)
            print("步骤 1/3: 读取英文字幕文件...")
            print("=" * 60)

            from video_subtitle_translator.subtitle_parser import parse_srt

            segments = parse_srt(args.subtitle)

            if not segments:
                print(f"警告：无法解析字幕文件: {args.subtitle}")
                sys.exit(1)

            print(f"成功读取 {len(segments)} 个字幕片段")
            audio_path = temp_dir / f"{video_name}_audio.wav"  # 占位
        else:
            # 步骤1: 提取音频
            print("=" * 60)
            print("步骤 1/5: 提取音频...")
            print("=" * 60)
            audio_path = temp_dir / f"{video_name}_audio.wav"
            extract_audio(str(video_path), str(audio_path))

            # 步骤2: 语音转文字
            print("\n" + "=" * 60)
            print("步骤 2/5: 语音识别（Whisper）...")
            print("=" * 60)
            transcriber = Transcriber(model_size=args.model)
            segments = transcriber.transcribe(str(audio_path), language=args.language)

            if not segments:
                print("警告：未识别到任何语音内容")
                sys.exit(1)

        # 步骤3: 翻译
        if args.subtitle:
            print("\n" + "=" * 60)
            print("步骤 2/3: 翻译中文字幕（Ollama）...")
            print("=" * 60)
        else:
            print("\n" + "=" * 60)
            print("步骤 3/5: 翻译中文字幕（Ollama）...")
            print("=" * 60)
        translator = Translator()
        segments = translator.translate_segments(segments)

        # 步骤4: 生成字幕文件
        if args.subtitle:
            print("\n" + "=" * 60)
            print("步骤 3/3: 生成字幕文件...")
            print("=" * 60)
        else:
            print("\n" + "=" * 60)
            print("步骤 4/5: 生成字幕文件...")
            print("=" * 60)

        # 生成ASS格式字幕（样式更丰富）
        ass_path = temp_dir / f"{video_name}_bilingual.ass"
        generate_ass(segments, str(ass_path))

        # 也生成SRT格式备用
        srt_path = temp_dir / f"{video_name}_bilingual.srt"
        generate_srt(segments, str(srt_path))

        # 步骤5: 合成视频
        if args.subtitle:
            print("\n" + "=" * 60)
            print("烧录字幕到视频...")
            print("=" * 60)
        else:
            print("\n" + "=" * 60)
            print("步骤 5/5: 烧录字幕到视频...")
            print("=" * 60)
        # 使用备用方法，切换到字幕目录执行ffmpeg
        from video_subtitle_translator.video_merger_alt import merge_with_drawtext

        output_video = merge_with_drawtext(str(video_path), str(srt_path), args.output)

        # 清理临时文件（如果不保留）
        if not args.keep_srt:
            print("\n清理临时文件...")
            if not args.subtitle and audio_path.exists():
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

    except Exception as e:
        print(f"\n错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
