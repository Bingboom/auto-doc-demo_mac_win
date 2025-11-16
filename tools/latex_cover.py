from jinja2 import Template
from datetime import datetime
from pathlib import Path
import yaml

# 加载 config.yaml 配置文件
def load_config():
    with open('config.yaml', 'r') as file:
        return yaml.load(file, Loader=yaml.FullLoader)

# 获取配置
config = load_config()

# 使用 config.yaml 中的路径设置
ROOT = Path(config['root']).resolve()  # 获取项目根目录
LATEX_DIR = Path(config['latex']).resolve()  # 获取 LaTeX 配置路径

def render_cover(model_name: str, version: str, doc_type: str):
    """
    使用 Jinja2 渲染封面模板：cover_template.tex.j2 → cover.tex
    """
    template_path = LATEX_DIR / "cover_template.tex.j2"
    output_path = LATEX_DIR / "cover.tex"

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
