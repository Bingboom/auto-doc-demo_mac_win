# tools/paths.py

from pathlib import Path
import sys

# 仓库根目录（从该文件两级上）
ROOT = Path(__file__).resolve().parents[1]

# 定义关键路径
PATHS = {
    "root": ROOT,
    "csv_input": ROOT / "csv-input",
    "tools": ROOT / "tools",
    "templates": ROOT / "docs" / "_common" / "templates",
    "sphinx_docs": ROOT / "docs",
    "build_html": ROOT / "docs" / "N706B" / "build" / "html",
    "build_pdf": ROOT / "docs" / "N706B" / "build" / "pdf",
    # 没有中间rst文件夹，直接在 source 目录里生成和存储 rst 文件
    "rst_source": ROOT / "docs" / "N706B" / "source",  
    "images": ROOT / "docs" / "_common" / "_static",
    # 根据你项目需要可继续添加
}

# 加入 PATHS["root"] 到 sys.path，方便跨模块导入
if str(PATHS["root"]) not in sys.path:
    sys.path.insert(0, str(PATHS["root"]))
