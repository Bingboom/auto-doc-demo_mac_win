# ==========================================
#   Neoway N706B Sphinx Configuration
# ==========================================
from pathlib import Path
import sys

# -------------------------------------------------------------------
# 1. 项目根目录
# -------------------------------------------------------------------
THIS_DIR = Path(__file__).resolve().parent
# docs/N706B/source → docs/N706B → docs → auto-doc-demo_mac_win
PROJECT_ROOT = THIS_DIR.parents[2]

# 给 Sphinx 加可访问的工具路径
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "tools"))

# -------------------------------------------------------------------
# 2. 导入路径模块（由 path_utils 控制所有路径）
# -------------------------------------------------------------------
import tools.utils.path_utils as paths

# 让 conf_common.py 可访问 paths 模块
globals()["paths"] = paths

# -------------------------------------------------------------------
# 3. 继承公共配置
# -------------------------------------------------------------------
COMMON_CONF = PROJECT_ROOT / "docs" / "_common" / "conf_common.py"
if not COMMON_CONF.exists():
    raise FileNotFoundError(f"[FATAL] Missing common config: {COMMON_CONF}")

exec(COMMON_CONF.read_text(encoding="utf-8"))

# -------------------------------------------------------------------
# 4. 产品线专属信息
# -------------------------------------------------------------------
PRODUCT = "N706B"
CONF = paths.product_conf(PRODUCT)

project = f"Neoway {PRODUCT} AT Command Manual"
author = "Neoway Technology"
html_title = project

latex_documents = [
    (
        "index",
        f"Neoway_{PRODUCT}_Manual.tex",
        project,
        author,
        "manual",
    )
]

# -------------------------------------------------------------------
# 5. 输出路径（来自 config.yaml）
# -------------------------------------------------------------------
html_output = paths.build_html_path(PRODUCT)
latex_output = paths.build_pdf_path(PRODUCT)
