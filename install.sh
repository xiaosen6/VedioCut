#!/bin/bash
# VideoCut CLI 安装脚本 (Linux/macOS)

set -e

echo "============================================"
echo "VideoCut CLI 安装程序"
echo "============================================"
echo ""

# 获取脚本所在目录
INSTALL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 创建启动脚本
echo "正在创建启动脚本..."
cat > /tmp/videocut << 'EOF'
#!/bin/bash
python3 "INSTALL_DIR/video_subtitle_translator/cli.py" "$@"
EOF

# 替换 INSTALL_DIR
sed -i "s|INSTALL_DIR|$INSTALL_DIR|g" /tmp/videocut
chmod +x /tmp/videocut

echo "✓ 启动脚本已创建"
echo ""

# 移动到系统路径
if [ -d "/usr/local/bin" ]; then
    sudo mv /tmp/videocut /usr/local/bin/videocut
    echo "✓ 已安装到 /usr/local/bin/videocut"
elif [ -d "$HOME/.local/bin" ]; then
    mkdir -p "$HOME/.local/bin"
    mv /tmp/videocut "$HOME/.local/bin/videocut"
    echo "✓ 已安装到 $HOME/.local/bin/videocut"
    
    # 检查PATH
    if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
        echo ""
        echo "请将以下内容添加到 ~/.bashrc 或 ~/.zshrc:"
        echo 'export PATH="$HOME/.local/bin:$PATH"'
    fi
else
    echo "⚠ 未找到合适的安装目录"
    echo "请手动将 /tmp/videocut 移动到您的PATH目录"
    exit 1
fi

echo ""
echo "============================================"
echo "安装完成！"
echo "============================================"
echo ""
echo "使用方法:"
echo '  videocut "视频路径.mp4"'
echo ""
echo "示例:"
echo '  videocut "/home/user/videos/lecture.mp4"'
echo '  videocut "/home/user/videos/lecture.mp4" -o "output.mp4"'
echo ""
