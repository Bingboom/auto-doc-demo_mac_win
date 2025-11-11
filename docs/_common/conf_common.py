# ================================================================
# 📘 Neoway 文档公共配置模块 conf_common.py
#    - 定义字体、Logo 路径、版权文字等
#    - 被各型号 conf.py 或工具脚本引用
# ================================================================

from datetime import datetime
from pathlib import Path

# === 公司/品牌常量 ===
COMPANY_NAME = "深圳市有方科技股份有限公司"
COMPANY_EN = "Neoway Technology Co., Ltd."
PROJECT_AUTHOR = "Neoway 文档工程组"

# === 版权与 Logo ===
COPYRIGHT_TEXT = f"{COMPANY_NAME} 版权所有"
LOGO_FILE = "header-logo.png"
BG_FILE = "background.png"

# === 字体配置 ===
FONTS = {
    "zh_main": "PingFang SC",       # macOS 默认
    "zh_win": "Microsoft YaHei",    # Windows 默认
    "zh_linux": "Noto Sans CJK SC", # Linux
    "en_main": "Times New Roman",
    "en_sans": "Arial",
    "en_mono": "Menlo"
}

# === 项目路径 ===
PROJECT_ROOT = Path(__file__).resolve().parents[2]
COMMON_STATIC = PROJECT_ROOT / "docs" / "_common" / "_static"

# === 公共函数 ===
def get_version_tag(version: str) -> str:
    """标准化版本号：v1.4 → V1.4"""
    return ("V" + version.lstrip("vV")).strip()

def get_date_str() -> str:
    """返回当前日期（中文格式）"""
    return datetime.now().strftime("%Y年%m月%d日")

# === LaTeX 默认变量初始化 ===
latex_elements = {}
latex_additional_files = [
    '../../_common/_static/logo.png',
    '../../_common/_static/background.png',
    '../../_common/_static/header-logo.png'
]