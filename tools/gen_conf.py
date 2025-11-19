# tools/gen_conf.py
from pathlib import Path
import sys

THIS = Path(__file__).resolve()
PROJECT_ROOT = THIS.parents[1]

sys.path.insert(0, str(PROJECT_ROOT))

from tools.utils import path_utils as paths
from jinja2 import Template


TEMPLATE = Path(__file__).parent / "conf_template.py.j2"


def generate_conf(product: str, lang: str, doc_type: str):
    """ 依据模板生成 product/lang/conf.py """

    cfg = paths.config

    source_dir = paths.rst_source_path(product, lang)
    conf_py = source_dir / "conf.py"

    lang_file = PROJECT_ROOT / "docs" / "_langs" / f"{lang}.py"

    # 加载模板
    tpl = Template(TEMPLATE.read_text(encoding="utf-8"))

    conf_py.write_text(
        tpl.render(
            PRODUCT=product,
            LANG=lang,
            DOC_TYPE=doc_type,
            cfg=cfg,
            lang_file=f"docs/_langs/{lang}.py"
        ),
        encoding="utf-8"
    )

    print(f"[CONF] Generated: {conf_py}")
