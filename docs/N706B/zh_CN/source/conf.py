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
LANG = "zh_CN"
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
PRODUCT = "N706B"

project = f"AT命令手册"
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

# ---------------------------------------------------------
# 6. 渲染封面 cover.tex（自动根据产品变量生成）
# ---------------------------------------------------------
from jinja2 import Template

template_path = paths.latex_common_path() / "cover_template.tex.j2"
output_path   = paths.latex_common_path() / "cover.tex"

# 让 cover 支持不同产品和语言
issue = "1.0"            # 如需可从 config.yaml 读
date  = "2025-11-18"     # 如需可从 config.yaml 读

variables = {
    "product": PRODUCT,
    "title": project,
    "issue": issue,
    "date": date,
}

with open(template_path, "r", encoding="utf-8") as f:
    template = Template(f.read())

with open(output_path, "w", encoding="utf-8") as f:
    f.write(template.render(**variables))

print(f"[COVER] 渲染封面完成 → {output_path}")

