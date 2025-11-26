# ==========================================
# Neoway Sphinx 通用配置（paths 由 conf.py 注入）
# ==========================================

from pathlib import Path
from jinja2 import Template

# ---------------- Path Init ----------------
common_templates_path = Path(paths.common_templates()).as_posix()
common_static_path    = Path(paths.static_images_path()).as_posix()
common_latex_path     = Path(paths.latex_common_path()).as_posix()

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
]

templates_path   = [common_templates_path]
html_static_path = [common_static_path]

# ---------------- Language + Product ----------------
LANG    = globals().get("LANG", "zh_cn")
PRODUCT = globals().get("PRODUCT")

# ---------------- Header Logo ----------------
header_cfg   = paths.config["common"].get("header_logo", {})
logo_file    = header_cfg.get(PRODUCT, header_cfg.get("default", "header-logo.png"))
HEADER_LOGO  = Path(paths.static_images_path() / logo_file).as_posix()

# ---------------- Additional LaTeX Files ----------------
latex_additional_files = [
    Path(paths.latex_common_path() / "cover.tex").as_posix(),
    Path(paths.latex_common_path() / "fonts.tex").as_posix(),
    Path(paths.latex_common_path() / "headerfooter.tex").as_posix(),
    HEADER_LOGO,
]

# ---------------- Font Logic ----------------
IS_CN = LANG.lower() in ("zh_cn", "zh-hans")

if IS_CN:
    fontpkg = r"\input{fonts.tex}"
else:
    fontpkg = r"""
\usepackage{fontspec}
\setmainfont{Times New Roman}
"""

latex_engine = "xelatex"

# =====================================================
# ---------------------- Preamble ---------------------
# =====================================================
# 核心：所有 \usepackage 必须在这里（不能在语言包）
preamble = r"""
\usepackage{xcolor}
\usepackage{titlesec}
\usepackage{tikz}
\usepackage{eso-pic}
\usepackage{graphicx}

% Sphinx 节点统一颜色（避免 literal node 跑到正文）
\definecolor{nwyLink}{RGB}{0,90,158}
\sphinxsetup{
  InnerLinkColor={rgb}{0,0.27,0.55},
  OuterLinkColor={rgb}{0,0.27,0.55},
  VerbatimColor={RGB}{247,247,247},
  VerbatimBorderColor={RGB}{204,204,204},
  verbatimwithframe=true,
  verbatimsep=6pt,
  verbatimborder=0.6pt,
}

\input{headerfooter.tex}

\makeatletter
\let\cleardoublepage\clearpage
\makeatother
"""

# 章节格式由语言包提供（但不包含任何 package）
chapter_fmt = globals().get("CHAPTER_FORMAT")
if chapter_fmt:
    preamble += "\n" + chapter_fmt + "\n"

# ---------------- Final LaTeX Config ----------------
latex_elements = {
    "fontpkg": fontpkg,
    "preamble": preamble,
    "maketitle": r"\input{cover.tex}",
}

# =====================================================
# ---------------- Render headerfooter.tex ------------
# =====================================================
template_file = Path(paths.latex_common_path() / "headerfooter.tex.j2")
output_file   = Path(paths.latex_common_path() / "headerfooter.tex")

copyright_map = paths.config["common"].get("copyright", {})
footer_text = copyright_map.get(LANG, copyright_map.get("en", ""))

tpl = Template(template_file.read_text(encoding="utf-8"))
output_file.write_text(
    tpl.render(company_name=footer_text, header_logo=HEADER_LOGO),
    encoding="utf-8"
)
