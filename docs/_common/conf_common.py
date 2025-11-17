# ==========================================
# Neoway Sphinx 通用配置（paths 由 conf.py 注入）
# ==========================================

common_templates_path = paths.common_templates()
common_static_path    = paths.static_images_path()
common_latex_path     = paths.latex_common_path()

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
]

templates_path   = [str(common_templates_path)]
html_static_path = [str(common_static_path)]

# -------------------------------
# 复制 LaTeX 资源（封面 + 字体 + 页眉页脚 + 图片）
# -------------------------------
latex_additional_files = [
    str(common_latex_path / "cover.tex"),
    str(common_latex_path / "fonts.tex"),
    str(common_latex_path / "headerfooter.tex"),

    str(common_static_path / "background.png"),
    str(common_static_path / "header-logo.png"),
]

# -------------------------------
# 禁用 Sphinx 默认 maketitle，确保只有你的封面
# -------------------------------
latex_elements = {
    # 加载 CJK 字体与 fancyhdr
    "fontpkg": r"\input{fonts.tex}",

    # 提前 input headerfooter + tikz
    "preamble": r"""
    \input{headerfooter.tex}
    \usepackage{tikz}
    \usepackage{eso-pic}
    \usepackage{graphicx}

    % -------- 删除 maketitle 后多余空白页 --------
    \makeatletter
    \let\cleardoublepage\clearpage
    \makeatother
    """,


    # maketitle 完全替换（不走 sphinxmanual 的默认 titlepage）
    "maketitle": r"\input{cover.tex}",
}
