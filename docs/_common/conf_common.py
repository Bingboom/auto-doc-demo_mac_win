# ==========================================
# Neoway Sphinx 通用配置（paths 由 conf.py 注入）
# ==========================================

from pathlib import Path
from jinja2 import Template

common_templates_path = paths.common_templates()
common_static_path    = paths.static_images_path()
common_latex_path     = paths.latex_common_path()

# 强制 POSIX 化路径
common_templates_path = Path(common_templates_path).as_posix()
common_static_path    = Path(common_static_path).as_posix()
common_latex_path     = Path(common_latex_path).as_posix()

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
]

templates_path   = [common_templates_path]
html_static_path = [common_static_path]

# ============= Language + Product =============
LANG = globals().get("LANG", "zh_cn")
PRODUCT = globals().get("PRODUCT")

# ============= Header Logo =============
header_cfg = paths.config["common"].get("header_logo", {})
logo_filename = header_cfg.get(PRODUCT, header_cfg.get("default", "header-logo.png"))

HEADER_LOGO_LATEX = Path(paths.static_images_path() / logo_filename).as_posix()

# ============= LaTeX Resource List =============
latex_additional_files = [
    Path(paths.latex_common_path() / "cover.tex").as_posix(),
    Path(paths.latex_common_path() / "fonts.tex").as_posix(),
    Path(paths.latex_common_path() / "headerfooter.tex").as_posix(),
    HEADER_LOGO_LATEX,   # 已经是 POSIX
]

# ============= 字体逻辑 =============
IS_CHINESE = LANG.lower() in ("zh_cn", "zh-hans")

if IS_CHINESE:
    fontpkg = r"\input{fonts.tex}"
else:
    fontpkg = r"""
\usepackage{fontspec}
\setmainfont{Times New Roman}
"""

latex_engine = "xelatex"

# ============= preamble =============
preamble = r"""
\input{headerfooter.tex}
\usepackage{tikz}
\usepackage{eso-pic}
\usepackage{graphicx}

% --------- Prevent endless rerun warnings ------------
\makeatletter
\let\cleardoublepage\clearpage
\def\@test@re-run{false}
\def\@latex@warning#1{}
\def\@latex@warning@no@line#1{}
\makeatother
"""

# ============= 允许 conf.py 覆盖的章节格式 =============
chapter_fmt = globals().get("CHAPTER_FORMAT")
if chapter_fmt:
    preamble += "\n" + chapter_fmt + "\n"

# ==============================================================
# 🔥 中文文档：覆盖附录格式为 “附录 A”
# ==============================================================

if IS_CHINESE:
    preamble += r"""
% ---------------------------------------------------------
%   中文附录章节格式（替换原有 Chapter Title）
% ---------------------------------------------------------
\usepackage{titlesec}

% 主章节标题格式：显示为 "附录 A"
\titleformat{\chapter}
  {\huge\bfseries}%
  {附录\ \thechapter}%
  {1em}{}

% Section/subsection 自动编号：A.1, A.2 …
\renewcommand{\thesection}{\thechapter.\arabic{section}}
\renewcommand{\thesubsection}{\thesection.\arabic{subsection}}
"""

# ============= 输出 latex_elements =============
latex_elements = {
    "fontpkg": fontpkg,
    "preamble": preamble,
    "maketitle": r"\input{cover.tex}",
}

# ============= 渲染 headerfooter.tex =============
template_file = paths.latex_common_path() / "headerfooter.tex.j2"
output_file   = paths.latex_common_path() / "headerfooter.tex"

template_file = Path(template_file)
output_file   = Path(output_file)

copyright_map = paths.config["common"].get("copyright", {})
footer_text = copyright_map.get(LANG, copyright_map.get("en", ""))

tpl = Template(template_file.read_text(encoding="utf-8"))
output_file.write_text(
    tpl.render(
        company_name=footer_text,
        header_logo=HEADER_LOGO_LATEX,
    ),
    encoding="utf-8"
)
