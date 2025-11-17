# ==========================================
# Neoway Sphinx 通用配置（paths 由 conf.py 注入）
# ==========================================

# ---------- 路径（保持原逻辑） ----------
common_templates_path = paths.common_templates()
common_static_path    = paths.static_images_path()
common_latex_path     = paths.latex_common_path()

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
]

templates_path   = [str(common_templates_path)]
html_static_path = [str(common_static_path)]


# ==========================================
#   Language Support (zh_CN / en)
# ==========================================
# conf.py 会注入变量：LANG
# 默认 zh_CN
LANG = globals().get("LANG", "zh_CN")

IS_CHINESE = LANG.lower() in ("zh_cn", "zh-hans")


# ==========================================
#   LaTeX 配置（按你的逻辑，保持资源不变）
# ==========================================
latex_additional_files = [
    str(common_latex_path / "cover.tex"),
    str(common_latex_path / "fonts.tex"),
    str(common_latex_path / "headerfooter.tex"),

    str(common_static_path / "background.png"),
    str(common_static_path / "header-logo.png"),
]


# ---------- 区分中英的字体逻辑 ----------
if IS_CHINESE:
    fontpkg = r"\input{fonts.tex}"
else:
    # 英文环境下不用加载中文字体避免报错
    fontpkg = r"""
\usepackage{fontspec}
\setmainfont{Times New Roman}
"""
    
# ==========================================
# 禁用 Sphinx 默认 maketitle，确保只有你的封面
# ==========================================
latex_elements = {
    "fontpkg": fontpkg,

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

    "maketitle": r"\input{cover.tex}",
}
