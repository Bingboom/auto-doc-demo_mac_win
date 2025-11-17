from jinja2 import Template
from datetime import datetime

from utils.path_utils import latex_common_path


LATEX_DIR = latex_common_path()

def render_cover(model: str, version: str, doc_type: str):
    """渲染封面模板 cover_template.tex.j2 → cover.tex"""

    tpl_path = LATEX_DIR / "cover_template.tex.j2"
    out_path = LATEX_DIR / "cover.tex"

    version_tag = "V" + version.lstrip("vV")
    date_cn = datetime.now().strftime("%Y年%m月%d日")

    tpl = Template(tpl_path.read_text(encoding="utf-8"))
    tex = tpl.render(
        model_name=model,
        doc_type=doc_type,
        version_tag=version_tag,
        date_cn=date_cn,
    )

    out_path.write_text(tex, encoding="utf-8")
    print(f"✔ 封面已生成：{out_path}")
    return out_path
