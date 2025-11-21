# ================================================================
# 📘 Neoway Docs Common Config（共享基础配置）
# ================================================================
from pathlib import Path
from datetime import datetime
import sys

# === 导入路径工具：完全基于 config.yaml 管理路径 ===
from tools.utils import path_utils as paths

# === 基本变量 ===
author = "Neoway 文档工程组"
language = "zh_CN"
copyright = (
    f"{datetime.now().year}, Neoway Technology"
)

# === 基于 config.yaml 动态解析路径 ===
COMMON_ROOT = Path(__file__).resolve().parent
STATIC_DIR = paths.static_images_path()              # docs/_common/_static
LATEX_COMMON = paths.latex_common_path()             # docs/_common/latex_templates
FONTS_TEX = LATEX_COMMON / "fonts.tex"               # 自动生成字体文件

# === HTML static ===
html_static_path = [str(STATIC_DIR)]
html_logo = str(STATIC_DIR / "logo.png")

# === LaTeX static files ===
latex_engine = "xelatex"
latex_additional_files = [
    str(STATIC_DIR / "logo.png"),
    str(STATIC_DIR / "header-logo.png"),
    str(STATIC_DIR / "background.png"),
    str(FONTS_TEX)
]

# ============================================================
# 📌 字体：完全由 fonts.tex 控制（由 build_docs.py 自动生成）
# ============================================================
latex_elements = {
    'papersize': 'a4paper',
    'pointsize': '11pt',
    'extraclassoptions': 'openany,oneside',

    'geometry': r'''
\usepackage[a4paper,
    top=22mm,
    bottom=22mm,
    left=25mm,
    right=25mm,
    headheight=25pt
]{geometry}
''',

    # ==== 关键：字体由 fonts.tex 控制（动态路径 from config.yaml） ====
    'fontpkg': rf'''
\usepackage{{fontspec}}
\usepackage{{xeCJK}}
\input{{{FONTS_TEX.as_posix()}}}
''',

    # ==== preamble（页眉页脚等） ====
    'preamble': rf'''
\usepackage{{fancyhdr}}
\usepackage{{titlesec}}
\usepackage{{tocloft}}
\usepackage{{hyperref}}
\usepackage{{setspace}}
\usepackage{{graphicx}}
\usepackage{{xcolor}}
\usepackage{{tikz}}

% -------- 页眉页脚 --------
\pagestyle{{fancy}}
\fancyhf{{}}
\fancyhead[L]{{\includegraphics[scale=0.25]{{{STATIC_DIR / "header-logo.png"}}}}}
\fancyhead[R]{{\leftmark}}
\fancyfoot[L]{{深圳市有方科技股份有限公司版权所有}}
\fancyfoot[R]{{\thepage}}
\renewcommand{{\headrulewidth}}{{0.4pt}}
\renewcommand{{\footrulewidth}}{{0.4pt}}
\setlength{{\headheight}}{{25pt}}

% -------- 中文目录与章节格式 --------
\renewcommand{{\contentsname}}{{\centering 目~录}}
\titleformat{{\chapter}}{{\Huge\bfseries}}{{第\,\thechapter\,章}}{{1em}}{{}}

\let\cleardoublepage\clearpage
'''
}
