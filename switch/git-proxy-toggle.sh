#!/bin/bash
# =====================================================
# 🧭 Git Proxy Toggle Script
# 功能：一键切换 Git 代理开关（on/off）
# 适用于 macOS / Linux
# 作者：ChatGPT 智能助手
# =====================================================

# === 默认代理端口配置（可根据你的代理软件修改） ===
HTTP_PROXY="http://127.0.0.1:7890"
HTTPS_PROXY="http://127.0.0.1:7890"

# === 获取当前代理状态 ===
current_http=$(git config --global --get http.proxy)
current_https=$(git config --global --get https.proxy)

# === 判断输入参数 ===
case "$1" in
  on)
    echo "🔧 开启 Git 全局代理..."
    git config --global http.proxy $HTTP_PROXY
    git config --global https.proxy $HTTPS_PROXY
    echo "✅ Git 代理已开启："
    git config --global --get http.proxy
    ;;
  off)
    echo "🧹 关闭 Git 全局代理..."
    git config --global --unset http.proxy
    git config --global --unset https.proxy
    echo "✅ Git 代理已关闭。"
    ;;
  status)
    echo "🔍 当前 Git 代理状态："
    if [ -z "$current_http" ]; then
      echo "❌ 未开启代理"
    else
      echo "🌐 HTTP代理: $current_http"
      echo "🔐 HTTPS代理: $current_https"
    fi
    ;;
  *)
    echo "🧭 用法："
    echo "  bash git-proxy-toggle.sh on      # 开启代理"
    echo "  bash git-proxy-toggle.sh off     # 关闭代理"
    echo "  bash git-proxy-toggle.sh status  # 查看当前状态"
    ;;
esac
