# tools/latex_cover.py
from jinja2 import Template
from datetime import datetime
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from paths import PATHS


def render_cover(model_name: str, version: str, doc_type: str):
    """
    使用 Jinja2 渲染封面模板：cover_template.tex.j2 → cover.tex
    """
    latex_dir = PATHS["latex"]

    template_path = latex_dir / "cover_template.tex.j2"
    output_path = latex_dir / "cover.tex"

    version_tag = "V" + version.lstrip("vV")
    date_cn = datetime.now().strftime("%Y年%m月%d日")

    tpl = Template(template_path.read_text(encoding="utf-8"))
    tex = tpl.render(
        model_name=model_name,
        doc_type=doc_type,
        version_tag=version_tag,
        date_cn=date_cn,
    )

    output_path.write_text(tex, encoding="utf-8")

    print(f"✔ 封面已生成：{output_path}")
    return output_path
