# ==========================================
# Neoway Sphinx 通用配置（纯配置，无副作用版）
# ==========================================

from pathlib import Path
from jinja2 import Template
import re

# ================================================================
# ① 基础路径（保持你的原始逻辑）
# ================================================================
common_templates_path = Path(paths.common_templates()).as_posix()
common_static_path    = Path(paths.static_images_path()).as_posix()
common_latex_path = Path(paths.latex_theme_path()).as_posix()


templates_path   = [common_templates_path]
html_static_path = [common_static_path]

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.autosectionlabel",
]

# ================================================================
# ② 语言 & 产品
# ================================================================
LANG    = globals().get("LANG", "zh_cn")
PRODUCT = globals().get("PRODUCT")

# ================================================================
# ③ LOGO（来自 config.yaml）
# ================================================================
_header_cfg = paths.config["common"].get("header_logo", {})
_logo_file  = _header_cfg.get(PRODUCT, _header_cfg.get("default", "header-logo.png"))
HEADER_LOGO = (paths.static_images_path() / _logo_file).as_posix()

# ================================================================
# ④ 主题加载（不做任何渲染或写文件）
# ================================================================
from tools.utils.theme_loader import load_pdf_theme

theme_name = paths.config.get("theme", {}).get("pdf_default")

# theme_cfg = 颜色/页眉/标题/其他设置
# theme_files = { "theme": Path(...), "titles": Path(...), ... }
try:
    theme_cfg, theme_files = load_pdf_theme(theme_name) if theme_name else ({}, {})
    print(f"[THEME] Loaded theme: {theme_name}")
except Exception as e:
    print(f"[THEME] load failed: {e}")
    theme_cfg, theme_files = {}, {}

# 给主题补默认值（兼容旧版 behavior）
theme_cfg = theme_cfg or {}
theme_cfg.setdefault("header_color", [0, 0, 0])
theme_cfg.setdefault("title_color",  [0, 0, 0])
theme_cfg.setdefault("footer_color", [0, 0, 0])
theme_cfg.setdefault("logo_height", 14)
theme_cfg.setdefault("extra_tex", "")
theme_cfg.setdefault("cover_background", "")

# ================================================================
# ⑤ 字体逻辑
# ================================================================
IS_CN = LANG.lower() in ("zh_cn", "zh-hans")

if IS_CN:
    fontpkg = r"\input{fonts.tex}"
else:
    fontpkg = r"""
\usepackage{fontspec}
\setmainfont{Times New Roman}
"""

latex_engine = "xelatex"

# ================================================================
# ⑥ preamble（保持原始逻辑）
# ================================================================
preamble = r"""
\usepackage{xcolor}
\usepackage{titlesec}
\usepackage{tikz}
\usepackage{eso-pic}
\usepackage{graphicx}

\input{headerfooter.tex}

\sphinxsetup{
  InnerLinkColor={rgb}{0,0.27,0.55},
  OuterLinkColor={rgb}{0,0.27,0.55}
}

\makeatletter
\let\cleardoublepage\clearpage
\makeatother
"""

chapter_fmt = globals().get("CHAPTER_FORMAT")
if chapter_fmt:
    preamble += "\n" + chapter_fmt + "\n"

# ================================================================
# ⑦ latex_elements（引用 theme.tex，但不生成它）
# ================================================================
latex_elements = {
    "fontpkg": fontpkg,
    "preamble": preamble + "\n" + r"\input{theme.tex}" + "\n",
    "maketitle": r"\input{cover.tex}",
}

# ================================================================
# ⑧ 附加文件（不负责生成，只告诉 Sphinx 需要哪些文件）
# ================================================================
latex_additional_files = []

theme_dir = Path(paths.latex_theme_path())

for p in theme_dir.glob("**/*"):
    if p.is_file() and p.suffix.lower() in [".tex", ".sty", ".cls", ".png", ".jpg"]:
        latex_additional_files.append(p.as_posix())

# logo 文件也加入（相对路径）
latex_additional_files.append(HEADER_LOGO)


# ================================================================
# ⑨ 渲染 headerfooter（允许保留，因为是简单文本替换）
#    ✔ 但不允许写 theme.tex / titles.tex / colors.tex 等会重复执行的文件
# ================================================================
template_file = Path(paths.latex_theme_path() / "headerfooter.tex.j2")
output_file   = Path(paths.latex_theme_path() / "headerfooter.tex")


copyright_map = paths.config["common"].get("copyright")
footer_text = copyright_map.get(LANG, copyright_map.get("en", ""))

tpl = Template(template_file.read_text(encoding="utf-8"))
output_file.write_text(
    tpl.render(company_name=footer_text, header_logo=HEADER_LOGO),
    encoding="utf-8"
)

