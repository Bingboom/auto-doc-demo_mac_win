from datetime import datetime
import platform
from pathlib import Path
import sys

# 引入 tools/paths.py 中的配置
sys.path.insert(0, str(Path(__file__).resolve().parents[2])) 

# 引入 paths.py 中的配置
from tools.paths import PATHS

COMPANY_NAME = "深圳市有方科技股份有限公司"
COPYRIGHT_CN = f"{COMPANY_NAME} 版权所有"

def get_fonts():
    sys_name = platform.system().lower()
    if "darwin" in sys_name or "mac" in sys_name:
        return {"zh_font": "PingFang SC", "mono_font": "Menlo"}
    elif "win" in sys_name:
        return {"zh_font": "Microsoft YaHei", "mono_font": "Consolas"}
    else:
        return {"zh_font": "Noto Sans CJK SC", "mono_font": "DejaVu Sans Mono"}

def get_version_tag(ver):
    return ("V" + ver.lstrip("vV")).strip()

def get_date_cn():
    return datetime.now().strftime("%Y年%m月%d日")

latex_additional_files = [
    str(PATHS["images"] / "logo.png"),
    str(PATHS["images"] / "background.png"),
    str(PATHS["images"] / "header-logo.png"),
]
