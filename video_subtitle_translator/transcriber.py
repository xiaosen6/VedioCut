"""
Speech-to-Text using faster-whisper
"""

import os
from pathlib import Path
from typing import List, Tuple
from faster_whisper import WhisperModel

from .config import MODELS_DIR, WHISPER_MODEL_SIZE, WHISPER_DEVICE, WHISPER_COMPUTE_TYPE


class Transcriber:
    """语音识别器"""

    def __init__(
        self, model_size: str = None, device: str = None, compute_type: str = None
    ):
        """
        初始化Whisper模型

        Args:
            model_size: 模型大小 (tiny, base, small, medium, large)
            device: 计算设备 (cpu, cuda)
            compute_type: 计算类型 (float16, int8)
        """
        self.model_size = model_size or WHISPER_MODEL_SIZE
        self.device = device or WHISPER_DEVICE
        self.compute_type = compute_type or WHISPER_COMPUTE_TYPE
        self.model = None

    def load_model(self):
        """加载Whisper模型"""
        if self.model is not None:
            return

        # 模型下载路径
        model_dir = os.path.join(MODELS_DIR, f"faster-whisper-{self.model_size}")
        os.makedirs(model_dir, exist_ok=True)

        print(f"Loading Whisper model: {self.model_size}")
        print(f"Model will be cached at: {model_dir}")

        # 设置环境变量让faster-whisper使用自定义缓存目录
        os.environ["WHISPER_CACHE_DIR"] = model_dir

        self.model = WhisperModel(
            self.model_size,
            device=self.device,
            compute_type=self.compute_type,
            download_root=model_dir,
            local_files_only=False,  # 允许下载
        )
        print("Model loaded successfully!")

    def transcribe(self, audio_path: str, language: str = "en") -> List[dict]:
        """
        转录音频

        Args:
            audio_path: 音频文件路径
            language: 音频语言代码

        Returns:
            转录结果列表，每个元素包含:
            {
                "start": 开始时间(秒),
                "end": 结束时间(秒),
                "text": 文本内容,
                "words": [可选]单词级别时间戳
            }
        """
        if self.model is None:
            self.load_model()

        print(f"Transcribing audio: {audio_path}")

        segments, info = self.model.transcribe(
            audio_path,
            language=language,
            task="transcribe",
            vad_filter=True,  # 语音活动检测，过滤静音
            vad_parameters=dict(min_silence_duration_ms=500),
        )

        print(
            f"Detected language: {info.language} (probability: {info.language_probability:.2f})"
        )

        results = []
        for segment in segments:
            results.append(
                {
                    "start": segment.start,
                    "end": segment.end,
                    "text": segment.text.strip(),
                }
            )

        print(f"Transcription complete: {len(results)} segments")
        return results
