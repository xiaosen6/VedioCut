"""
Text translation using Ollama API
"""

import requests
import time
from typing import List, Dict
from .config import OLLAMA_HOST, OLLAMA_MODEL


class Translator:
    """翻译器"""

    def __init__(self, host: str = None, model: str = None):
        """
        初始化翻译器

        Args:
            host: Ollama API地址
            model: 使用的模型名称
        """
        self.host = host or OLLAMA_HOST
        self.model = model or OLLAMA_MODEL
        self.api_url = f"{self.host}/api/generate"

    def translate_text(self, text: str, retries: int = 3, delay: float = 0.5) -> str:
        """
        翻译单句文本

        Args:
            text: 要翻译的英文文本
            retries: 重试次数
            delay: 重试延迟（秒）

        Returns:
            中文翻译结果
        """
        prompt = f"""将以下英文翻译成简洁自然的中文，直接输出翻译结果，不要解释、不要提供多个版本、不要添加额外内容：

{text}"""

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.1,  # 更低随机性
                "num_predict": 100,  # 严格限制生成长度
            },
        }

        for attempt in range(retries):
            try:
                response = requests.post(self.api_url, json=payload, timeout=60)
                response.raise_for_status()
                result = response.json()

                translated = result.get("response", "").strip()
                # 清理可能的提示词残留
                translated = (
                    translated.replace("中文：", "").replace("Chinese:", "").strip()
                )
                return translated

            except requests.exceptions.RequestException as e:
                if attempt < retries - 1:
                    print(f"Translation failed, retrying ({attempt + 1}/{retries})...")
                    time.sleep(delay * (attempt + 1))
                else:
                    print(f"Translation failed after {retries} attempts: {e}")
                    return text  # 失败返回原文

        return text

    def translate_segments(self, segments: List[Dict]) -> List[Dict]:
        """
        批量翻译转录结果

        Args:
            segments: 转录结果列表

        Returns:
            添加翻译后的列表
        """
        print(f"Translating {len(segments)} segments...")

        for i, segment in enumerate(segments):
            original_text = segment["text"]
            translated_text = self.translate_text(original_text)
            segment["translation"] = translated_text

            if (i + 1) % 10 == 0:
                print(f"Translated {i + 1}/{len(segments)} segments")

        print("Translation complete!")
        return segments
