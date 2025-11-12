from pathlib import Path
from config_manager import get_config_paths
from latex_injector import create_latex_block, inject_latex
from sphinx_builder import build_latex_from_sphinx
from xelatex_compiler import compile_xelatex
from pdf_manager import generate_pdf

# 定义 model_name 和其他参数
model_name = "N706B"
version = "v1.4"
doc_type = "AT 命令手册"
author = "Neoway 文档工程组"

PROJECT_ROOT = Path(__file__).resolve().parent.parent
project_dir, build_dir = get_config_paths(PROJECT_ROOT, model_name)

LATEX_DIR = build_dir / "latex"
PDF_DIR = build_dir / "pdf"
PDF_DIR.mkdir(parents=True, exist_ok=True)
CONF_PATH = project_dir / "conf.py"


# 1. 注入 LaTeX 样式
latex_block = create_latex_block(
    model_name=model_name,
    version=version,
    doc_type=doc_type,
    author=author,
    company="Neoway Technology",  # 可选，默认值是 Neoway Technology
    zh_font="PingFang SC",       # 可选，默认值是 PingFang SC
    mono_font="Menlo",           # 可选，默认值是 Menlo
    date_cn=None                 # 可选，默认为当前日期
)

inject_latex(CONF_PATH, latex_block)

# 2. 构建 Sphinx → LaTeX
build_latex_from_sphinx(project_dir, LATEX_DIR)

# 3. 编译 XeLaTeX
compile_xelatex(LATEX_DIR)

# 4. 生成 PDF
generate_pdf(LATEX_DIR, PDF_DIR, version, model_name, doc_type)
