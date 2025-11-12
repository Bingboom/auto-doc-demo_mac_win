#!/bin/bash
# 自动检测系统类型并调用对应的环境配置脚本

if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "🖥 macOS 系统，运行 macOS 环境初始化..."
    bash environment/setup_env_mac.sh
elif [[ "$OSTYPE" == "msys"* || "$OSTYPE" == "cygwin"* ]]; then
    echo "🖥 Windows 系统，运行 Windows 环境初始化..."
    powershell.exe -ExecutionPolicy RemoteSigned -File environment/setup_env_win.ps1
else
    echo "❌ 目前仅支持 macOS 和 Windows 系统！"
    exit 1
fi
