# ==========================================
# 📘 setup_env_win.ps1 — Windows 环境初始化脚本
# ==========================================

Write-Host "🔧 检查 GTK 安装包 (WeasyPrint 依赖)"
$gtkPath = "C:\Program Files\GTK3-Runtime"
if (!(Test-Path $gtkPath)) {
    Write-Host "❌ 未找到 GTK3，正在下载..."
    $url = "https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer/releases/download/2022-12-01/gtk3-runtime-3.24.34-2022-12-01-ts-win64.exe"
    $installer = "$env:TEMP\gtk3-runtime-installer.exe"
    Invoke-WebRequest -Uri $url -OutFile $installer
    Start-Process -FilePath $installer -ArgumentList "/SILENT","/DIR=$gtkPath" -Wait
} else {
    Write-Host "✅ GTK3 已安装在: $gtkPath"
}

Write-Host "🔧 配置环境变量 PATH"
[System.Environment]::SetEnvironmentVariable("PATH", "$env:PATH;$gtkPath\bin", "User")

Write-Host "📦 创建虚拟环境并安装依赖"
python -m venv .venv
.\.venv\Scripts\activate
pip install -U pip setuptools wheel
pip install -r requirements.txt

Write-Host "✅ 环境初始化完成，请执行: make pdf"
