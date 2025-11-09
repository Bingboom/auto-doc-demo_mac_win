# ================================================================
# 📘 Neoway N706B conf.py — 修正版，确保 _common 路径正确
# ================================================================
from pathlib import Path
import sys, os
from datetime import datetime

# === 修正导入路径 ===
CURRENT_DIR = Path(__file__).resolve()
COMMON_PATH = CURRENT_DIR.parents[2] / "_common"   # 🔧 改成此行
if not COMMON_PATH.exists():
    raise FileNotFoundError(f"❌ 找不到公共配置路径: {COMMON_PATH}")
sys.path.insert(0, str(COMMON_PATH))

from conf_common import *  # ✅ 成功导入




# === 项目信息 ===
project = "Neoway AT 命令手册"
author = "Neoway 文档工程组"
release = "v1.4"
today = datetime.now().strftime("%Y-%m-%d")
copyright = f"{datetime.now().year}, Neoway Technology"

# === 基础设置 ===
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.todo",
    "sphinx.ext.ifconfig",
    "sphinx.ext.viewcode",
]
templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]
language = "zh_CN"
html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
html_logo = "_static/logo.png"
html_show_sourcelink = False
html_last_updated_fmt = today

# === LaTeX 输出配置 ===
latex_engine = "xelatex"
latex_documents = [
    ("index", "Neoway_N706B_Manual.tex", project, author, "manual"),
]

# === 附加文件（封面图等） ===
latex_additional_files += [
    str(Path("_common/_static/logo.png")),
    str(Path("_common/_static/header-logo.png")),
    str(Path("_common/_static/background.png")),
]

# === 补充封面定义（不破坏目录） ===
latex_elements.update({
    'maketitle': r"""
\begin{titlepage}
\thispagestyle{empty}
\begin{tikzpicture}[remember picture, overlay]
  \node[anchor=north west, inner sep=0pt] at (current page.north west)
    {\includegraphics[width=\paperwidth,height=\paperheight]{_common/_static/background.png}};
\end{tikzpicture}
\vspace*{8cm}
\begin{flushleft}
  {\color[HTML]{70AD47}\fontsize{42}{48}\selectfont \textbf{N706B}}\\[0.8cm]
  {\fontsize{28}{32}\selectfont AT 命令手册}\\[0.6cm]
  {\large 版本 V1.4 \hspace{1em} 日期 """ + today + r"""}
\end{flushleft}
\end{titlepage}
\clearpage
"""
})

# >>> BEGIN: NEOWAY_LATEX_BLOCK
# 自动注入时间：2025-11-10 00:06:01
latex_engine = 'xelatex'
latex_additional_files = [
    '../../_common/_static/logo.png',
    '../../_common/_static/header-logo.png',
    'background.png'
]
latex_documents = [('index', 'Neoway_N706B_Manual.tex', 'Neoway N706B AT 命令手册', 'Neoway 文档工程组', 'manual')]

latex_elements = globals().get('latex_elements', {})

latex_elements.update({
    'papersize': 'a4paper',
    'pointsize': '11pt',
    'extraclassoptions': 'openany,oneside',
    'geometry': r'\usepackage[a4paper,top=22mm,bottom=22mm,left=22mm,right=22mm,headheight=25pt]{geometry}',
    'fontpkg': r'''
\usepackage{xeCJK}
\setCJKmainfont{PingFang SC}
\setmainfont{Times New Roman}
\setsansfont{Arial}
\setmonofont{Menlo}
    ''',
    'preamble': r'''
\usepackage{graphicx,tikz,eso-pic,xcolor,fancyhdr,titlesec,hyperref}
\graphicspath{{./}{../../_common/_static/}{../../../_common/_static/}}
\setlength{\headheight}{25pt}
\setlength{\headsep}{12pt}

\hypersetup{
  pdftitle={ Neoway N706B AT 命令手册 },
  pdfauthor={ Neoway 文档工程组 },
  pdfsubject={ Neoway 机密 | N706B | V1.4 },
  colorlinks=true, linkcolor=blue, urlcolor=blue
}

\newcommand{\neowayheaderlogo}{\includegraphics[scale=0.25]{header-logo.png}}
\makeatletter
\renewcommand{\chaptermark}[1]{\markboth{#1}{}}
\renewcommand{\sectionmark}[1]{\markright{#1}}
\makeatother

\fancypagestyle{normal}{%
  \fancyhf{}%
  \fancyhead[L]{\neowayheaderlogo}%
  \fancyhead[R]{\nouppercase{\rightmark}}%
  \fancyfoot[L]{深圳市有方科技股份有限公司版权所有}%
  \fancyfoot[R]{\thepage}%
  \renewcommand{\headrulewidth}{0.4pt}%
  \renewcommand{\footrulewidth}{0.4pt}%
}

\fancypagestyle{plain}{%
  \fancyhf{}%
  \fancyhead[L]{\neowayheaderlogo}%
  \fancyhead[R]{\nouppercase{\rightmark}}%
  \fancyfoot[L]{深圳市有方科技股份有限公司版权所有}%
  \fancyfoot[R]{\thepage}%
  \renewcommand{\headrulewidth}{0.4pt}%
  \renewcommand{\footrulewidth}{0.4pt}%
}
    \let\cleardoublepage\clearpage
    ''',
    'maketitle': r"""
%% -------- Neoway 封面 --------
\thispagestyle{empty}
\pagenumbering{gobble}
\begin{titlepage}
  \begin{tikzpicture}[remember picture, overlay]
    \node[anchor=north west, inner sep=0pt] at (current page.north west)
      {\includegraphics[width=\paperwidth,height=\paperheight]{background.png}};
  \end{tikzpicture}
  \vspace*{8cm}
  \begin{flushleft}
    {\color[HTML]{70AD47}\fontsize{42}{48}\selectfont \textbf{N706B}}\\[0.8cm]
    {\fontsize{28}{32}\selectfont AT 命令手册}\\[0.6cm]
    {\large 版本 V1.4 \hspace{1em} 日期 2025年11月10日}
  \end{flushleft}
\end{titlepage}
\clearpage
\pagenumbering{roman}
""",
})
# <<< END:  NEOWAY_LATEX_BLOCK

