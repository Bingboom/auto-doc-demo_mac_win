# ==========================================
# Neoway Sphinx Config (LANG from folder)
# ==========================================
from pathlib import Path
import sys

# ---------------------------------------------------------
# 1. 从路径解析语言与产品（docs/<lang>/<product>/source/conf.py）
# ---------------------------------------------------------
THIS_FILE = Path(__file__).resolve()

LANG    = THIS_FILE.parents[2].name    # zh_CN / en
PRODUCT = THIS_FILE.parents[1].name    # N706B

# ---------------------------------------------------------
# 2. 定位仓库根目录
# ---------------------------------------------------------
PROJECT_ROOT = THIS_FILE.parents[4]     # auto-doc-demo_mac_win/

sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "tools"))

# ---------------------------------------------------------
# 3. 加载路径工具（你当前仓库的 path_utils 完全兼容）
# ---------------------------------------------------------
import tools.utils.path_utils as paths
globals()["paths"] = paths

# ---------------------------------------------------------
# 4. 加载语言配置文件 docs/_langs/<LANG>.py
# ---------------------------------------------------------
lang_file = PROJECT_ROOT / "docs" / "_langs" / f"{LANG}.py"

if not lang_file.exists():
    raise FileNotFoundError(f"Language config not found: {lang_file}")

lang_namespace = {}
exec(lang_file.read_text(encoding="utf-8"), lang_namespace)

# 注入所有语言模块中的大写变量，如 TITLE / ISSUE / DATE
for key, val in lang_namespace.items():
    if key.isupper():
        globals()[key] = val

globals()["LANG"] = LANG   # 给 conf_common.py 使用


# ---------------------------------------------------------
# 5. 继承通用配置（你的原 conf_common.py）
# ---------------------------------------------------------
COMMON_CONF = PROJECT_ROOT / "docs" / "_common" / "conf_common.py"
exec(COMMON_CONF.read_text(encoding="utf-8"), globals())


# ---------------------------------------------------------
# 6. latex_documents（标题字段来自语言文件）
# ---------------------------------------------------------
latex_documents = [
    (
        "index",
        f"Neoway_{PRODUCT}_Manual.tex",
        PROJECT_TITLE,            # <-- 从语言文件注入
        "Neoway Technology",
        "manual",
    )
]


# ---------------------------------------------------------
# 7. 渲染封面 cover.tex（语言文件提供 ISSUE、DATE、PROJECT_TITLE）
# ---------------------------------------------------------
from jinja2 import Template

template_path = paths.latex_common_path() / "cover_template.tex.j2"
output_path   = paths.latex_common_path() / "cover.tex"

variables = {
    "product": PRODUCT,
    "title": PROJECT_TITLE,
    "issue": ISSUE,
    "date": DATE,
}

with open(template_path, "r", encoding="utf-8") as f:
    template = Template(f.read())

with open(output_path, "w", encoding="utf-8") as f:
    f.write(template.render(**variables))

print(f"[COVER] 渲染封面完成 → {output_path}")
