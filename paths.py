# paths.py （放在项目根目录）
from pathlib import Path
import sys

# 仓库根目录（当前文件所在目录）
ROOT = Path(__file__).resolve().parent

# 确保根目录可被 import 到
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# 统一路径配置
PATHS = {
    "root": ROOT,
    "tools": ROOT / "tools",
    "csv_input": ROOT / "csv-input",

    # Sphinx
    "docs": ROOT / "docs",
    "templates": ROOT / "docs" / "_common" / "templates",
    "latex": ROOT / "docs" / "_common" / "latex",
    "images": ROOT / "docs" / "_common" / "_static",

    # 默认使用 N706B（未来可做动态机型）
    "rst_source": ROOT / "docs" / "N706B" / "source",
    "build_html": ROOT / "docs" / "N706B" / "build" / "html",
    "build_pdf": ROOT / "docs" / "N706B" / "build" / "pdf",
}
