# ==========================================
# Neoway NN706BB 文档配置（en）
# ==========================================
from pathlib import Path
import sys

# ---------------------------------------------------------
# 1. 定位仓库根目录：docs/NN706BB/en/source/conf.py
# ---------------------------------------------------------
THIS_FILE = Path(__file__).resolve()
PROJECT_ROOT = THIS_FILE.parents[4]   # auto-doc-demo_mac_win/

# 确保 tools/utils/path_utils 可以 import
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "tools"))

# ---------------------------------------------------------
# 2. 注入 paths（conf_common.py 会用）
# ---------------------------------------------------------
import tools.utils.path_utils as paths
globals()["paths"] = paths

# ---------------------------------------------------------
# 3. 注入语言（关键！）
# ---------------------------------------------------------
LANG = "en"
globals()["LANG"] = LANG

# ---------------------------------------------------------
# 4. 继承公共配置 docs/_common/conf_common.py
# ---------------------------------------------------------
COMMON_CONF = PROJECT_ROOT / "docs" / "_common" / "conf_common.py"

if not COMMON_CONF.exists():
    raise FileNotFoundError(f"Missing common config: {COMMON_CONF}")

exec(COMMON_CONF.read_text(encoding="utf-8"), globals())

# ---------------------------------------------------------
# 5. 产品信息（保持你的原逻辑）
# ---------------------------------------------------------
PRODUCT = "NN706BB"

project = f"Neoway {PRODUCT} AT Command Manual"
author = "Neoway Technology"
html_title = project

latex_documents = [
    (
        "index",
        f"Neoway_N706B_Manual.tex",
        project,
        author,
        "manual",
    )
]
