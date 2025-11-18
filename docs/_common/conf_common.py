# ==========================================
# Neoway Sphinx 通用配置（paths 由 conf.py 注入）
# ==========================================

# ---------- 路径（保持原逻辑，来自 path_utils） ----------
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
# conf.py 注入变量 LANG
LANG = globals().get("LANG", "zh_CN")

IS_CHINESE = LANG.lower() in ("zh_cn", "zh-hans")


# ==========================================
#   LaTeX 资源（保持你的原文件结构）
# ==========================================
latex_additional_files = [
    str(common_latex_path / "cover.tex"),
    str(common_latex_path / "fonts.tex"),
    str(common_latex_path / "headerfooter.tex"),

    # 静态资源（保持不变）
    str(common_static_path / "background.png"),
    str(common_static_path / "header-logo.png"),
]


# ==========================================
# 字体逻辑（不丢失你的中文字体方案）
# ==========================================
if IS_CHINESE:
    # 使用你仓库中 fonts.tex（提供中文字体）
    fontpkg = r"\input{fonts.tex}"
else:
    # 英文模式采用原生系统字体
    fontpkg = r"""
\usepackage{fontspec}
\setmainfont{Times New Roman}
"""


# ==========================================
# 关键：禁用默认 maketitle，使用 cover.tex
# ==========================================
latex_elements = {
    "fontpkg": fontpkg,

    "preamble": r"""
    % ===== Header & Footer =====
    \input{headerfooter.tex}

    % ===== Extra Packages =====
    \usepackage{tikz}
    \usepackage{eso-pic}
    \usepackage{graphicx}

    % -------- 删除 maketitle 后多余空白页 --------
    \makeatletter
    \let\cleardoublepage\clearpage
    \makeatother
    """,

    # -------- 使用你提供的封面 cover.tex --------
    "maketitle": r"\input{cover.tex}",
}
