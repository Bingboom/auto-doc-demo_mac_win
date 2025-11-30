# tools/gen_conf.py
from pathlib import Path
import sys
from jinja2 import Template

THIS = Path(__file__).resolve()
TOOLS_ROOT = THIS.parent
PROJECT_ROOT = THIS.parents[1]

sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(TOOLS_ROOT))

from tools.utils import path_utils as paths


TEMPLATE = TOOLS_ROOT / "conf_template.py.j2"


def generate_conf(product: str, lang: str, doc_type: str):

    cfg = paths.config
    source_dir = paths.rst_source_path(product, lang)
    conf_py = source_dir / "conf.py"

    # ----------------------------------------------------
    # ★ 获取当前产品主题
    # ----------------------------------------------------
    theme_name = (
        cfg["products"].get(product, {}).get("pdf_theme") or
        cfg["theme"].get("pdf_default")
    )

    # ----------------------------------------------------
    # ★ 语言包路径（相对 ROOT）
    # ----------------------------------------------------
    lang_file_rel = str(
        paths.langs_dir().relative_to(paths.ROOT) / f"{lang}.py"
    )

    # ----------------------------------------------------
    # ★ 渲染 conf.py
    # ----------------------------------------------------
    text = Template(TEMPLATE.read_text(encoding="utf-8")).render(
        PRODUCT=product,
        LANG=lang,
        DOC_TYPE=doc_type,
        lang_file=lang_file_rel,
        pdf_theme=theme_name,   # <—— 注入主题
    )

    conf_py.write_text(text, encoding="utf-8")
    print(f"[CONF] Generated → {conf_py}")


if __name__ == "__main__":
    generate_conf("N706B", "zh_cn", "AT")
