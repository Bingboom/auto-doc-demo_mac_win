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

# ============= Language + Product =============
LANG = globals().get("LANG", "zh_cn")
PRODUCT = globals().get("PRODUCT")      # conf.py 注入

# ============= Header Logo 读取 =============
header_cfg = paths.config["common"].get("header_logo", {})

# 产品专用 → default → fallback
logo_filename = header_cfg.get(PRODUCT, header_cfg.get("default", "header-logo.png"))

# 最终 LaTeX 使用的路径（相对 + 绝对都可）
HEADER_LOGO_LATEX = str(common_static_path / logo_filename)


# ============= LaTeX Resource List =============
latex_additional_files = [
    str(common_latex_path / "cover.tex"),
    str(common_latex_path / "fonts.tex"),
    str(common_latex_path / "headerfooter.tex"),

    # 加载背景图与 header logo
    str(common_static_path / "background.png"),
    str(common_static_path / logo_filename),
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
    \makeatletter
    \let\cleardoublepage\clearpage
    \makeatother
"""

chapter_fmt = globals().get("CHAPTER_FORMAT")
if chapter_fmt:
    preamble += "\n" + chapter_fmt + "\n"

latex_elements = {
    "fontpkg": fontpkg,
    "preamble": preamble,
    "maketitle": r"\input{cover.tex}",
}


# ============= 渲染 headerfooter.tex =============
from jinja2 import Template

template_file = common_latex_path / "headerfooter.tex.j2"
output_file   = common_latex_path / "headerfooter.tex"

# ---- copyright ----
copyright_map = paths.config["common"].get("copyright", {})
footer_text = copyright_map.get(LANG, copyright_map.get("en", ""))

# ---- 渲染模板 ----
with open(template_file, "r", encoding="utf-8") as f:
    tpl = Template(f.read())

output_file.write_text(
    tpl.render(
        company_name=footer_text,
        header_logo=HEADER_LOGO_LATEX,   # ★★★ 核心：传入 header_logo ★★★
    ),
    encoding="utf-8"
)
