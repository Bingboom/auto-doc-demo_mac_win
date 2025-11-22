# tools/gen_conf.py
# ============================================================
# 依据统一路径体系生成 conf.py（产品 × 语言 × 文档类型）
# ============================================================
from pathlib import Path
import sys
from jinja2 import Template

# ------------------------------------------------------------
# 保证可以 import path_utils
# ------------------------------------------------------------
THIS = Path(__file__).resolve()
TOOLS_ROOT = THIS.parent             # tools/
PROJECT_ROOT = THIS.parents[1]       # 仓库根目录

sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(TOOLS_ROOT))

from tools.utils import path_utils as paths


# ------------------------------------------------------------
# 模板路径（保持你原始仓库位置）
# tools/conf_template.py.j2
# ------------------------------------------------------------
TEMPLATE = THIS.parent / "conf_template.py.j2"


# ------------------------------------------------------------
# 生成 conf.py
# ------------------------------------------------------------
def generate_conf(product: str, lang: str, doc_type: str):
    """
    根据 conf_template.py.j2 模板，为 product/lang 生成 Sphinx conf.py
    路径全部来自 path_utils.py
    """

    cfg = paths.config
    source_dir = paths.rst_source_path(product, lang)
    conf_py = source_dir / "conf.py"

    # conf.py 中 import 语言文件的路径
    lang_file_rel = f"docs/_langs/{lang}.py"

    # ---- 加载模板 ----
    tpl_text = TEMPLATE.read_text(encoding="utf-8")
    tpl = Template(tpl_text)

    # ---- 渲染 conf.py ----
    out_text = tpl.render(
        PRODUCT=product,
        LANG=lang,
        DOC_TYPE=doc_type,
        cfg=cfg,
        lang_file=lang_file_rel
    )

    conf_py.write_text(out_text, encoding="utf-8")

    print(f"[CONF] Generated: {conf_py}")


if __name__ == "__main__":
    # 本地测试
    generate_conf("N706B", "zh_cn", "AT")
