#!/bin/bash
# ==========================================
# 📘 setup_env_mac.sh — macOS 环境初始化脚本
# ==========================================

echo "🔍 检查 Homebrew ..."
if ! command -v brew &> /dev/null; then
  echo "❌ 未检测到 Homebrew，正在安装..."
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
else
  echo "✅ Homebrew 已安装"
fi

echo "🔧 安装 WeasyPrint 依赖库 ..."
brew install cairo pango gdk-pixbuf libffi libxml2 libxslt pygobject3 || exit 1
brew link cairo pango gdk-pixbuf libffi --force

echo "📦 创建 Python 虚拟环境 ..."
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip setuptools wheel

echo "📘 安装 Python 依赖 ..."
pip install -r requirements.txt

echo "✅ 环境初始化完成，可执行: make pdf"
