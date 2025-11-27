# ==========================================
# Neoway Sphinx 通用配置（启用 ESP 视觉包）
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
    "sphinx.ext.autosectionlabel"
]

templates_path   = [common_templates_path]
html_static_path = [common_static_path]

# ---------------- Language + Product ----------------
LANG    = globals().get("LANG", "zh_cn")
PRODUCT = globals().get("PRODUCT")

# ---------------- Header Logo ----------------
header_cfg  = paths.config["common"].get("header_logo", {})
logo_file   = header_cfg.get(PRODUCT, header_cfg.get("default", "header-logo.png"))
HEADER_LOGO = Path(paths.static_images_path() / logo_file).as_posix()

# ---------------- Additional LaTeX Files ----------------
latex_additional_files = [
    Path(paths.latex_common_path() / "cover.tex").as_posix(),
    Path(paths.latex_common_path() / "fonts.tex").as_posix(),
    Path(paths.latex_common_path() / "headerfooter.tex").as_posix(),
    Path(paths.latex_common_path() / "esp_colors.tex").as_posix(),
    Path(paths.latex_common_path() / "esp_titles.tex").as_posix(),
    Path(paths.latex_common_path() / "esp_verbatim.tex").as_posix(),
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
# 【必须注意】所有包加载只能放在 preamble，禁止语言包加载包
# 这样才能避免 xcolor / titlesec 内容跑到 PDF 第二页
preamble = r"""
\usepackage{xcolor}
\usepackage{titlesec}
\usepackage{tikz}
\usepackage{eso-pic}
\usepackage{graphicx}

% =============================
% 通用 header/footer
% =============================
\input{headerfooter.tex}

% =============================
% ESP 样式包（颜色、标题、code框）
% 必须在这里加载，顺序不能乱
% =============================
\input{esp_colors.tex}
\input{esp_titles.tex}
\input{esp_verbatim.tex}

% =============================
% Sphinx literal/link 样式兼容
% =============================
\sphinxsetup{
  InnerLinkColor={rgb}{0,0.27,0.55},
  OuterLinkColor={rgb}{0,0.27,0.55}
}

% =============================
% 禁止双页清空
% =============================
\makeatletter
\let\cleardoublepage\clearpage
\makeatother
"""

# ---------------- Chapter Format（语言包提供） ----------------
chapter_fmt = globals().get("CHAPTER_FORMAT")
if chapter_fmt:
    preamble += "\n" + chapter_fmt + "\n"

# ---------------- Final LaTeX Config ----------------
latex_elements = {
    "fontpkg": fontpkg,
    "preamble": preamble,
    "maketitle": r"\input{cover.tex}",
    "papersize": "a4paper",
    "pointsize": "11pt",
    "tocdepth": "2",
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
