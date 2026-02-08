from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="videocut",
    version="1.0.0",
    author="xiaosen6",
    author_email="",
    description="视频英译中字幕生成器 - 一键将英语视频转换为中文字幕视频",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/xiaosen6/VedioCut",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Multimedia :: Video",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=[
        "faster-whisper>=1.0.0",
        "requests>=2.31.0",
    ],
    entry_points={
        "console_scripts": [
            "videocut=video_subtitle_translator.cli:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
