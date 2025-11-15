import sys
from pathlib import Path

# ===== 自动添加项目根目录到 sys.path =====
ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from paths import PATHS
from tools.latex_cover import render_cover

# ===== 基础项目信息（仅用于 HTML，不参与 LaTeX 注入） =====
project = "Neoway N706B AT Command Manual"
author = "Neoway Documentation Team"
release = "v1.4"

# ===== Sphinx 基础配置 =====
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.todo",
    "sphinx.ext.mathjax",
]

templates_path = ["_templates"]
exclude_patterns = []
language = "zh_CN"

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]

# ===== LaTeX 资源（由 latex_styles.py / build_pdf 加载） =====
# 这些永远不应写死在 conf.py 内，保持动态注入
latex_engine = "xelatex"
latex_elements = {}
latex_additional_files = []
latex_documents = []

# ====== 预留注入区（自动生成） ======


# >>> AUTO_LATEX_BEGIN

latex_engine = "xelatex"

latex_documents = [
    ('index', 'Neoway_N706B_Manual.tex', 'Neoway N706B AT_Command_Manual', 'Neoway Documentation Team', 'manual')
]

latex_elements = {
    "fontpkg": r"""% ===== Neoway LaTeX 字体统一配置 =====
\usepackage{xeCJK}
\setCJKmainfont{PingFang SC}
\setCJKsansfont{PingFang SC}
\setCJKmonofont{PingFang SC}

\setmainfont{Times New Roman}
\setsansfont{Arial}
\setmonofont{Menlo}
""",
    "preamble": r"""% docs/_common/latex/base_preamble.tex
% 只负责通用包 + 超链接设置，不再引入 geometry，不定义页眉页脚

\usepackage{graphicx}
\usepackage{tikz}
\usepackage{eso-pic}
\usepackage{xcolor}
\usepackage{fancyhdr}
\usepackage{titlesec}
\usepackage{hyperref}

% 头部高度
\setlength{\headheight}{24pt}
\setlength{\headsep}{12pt}

% 超链接样式
\hypersetup{
  colorlinks=true,
  linkcolor=blue,
  urlcolor=blue,
  citecolor=blue,
  pdfborder={0 0 0}
}

% 让 TikZ 背景图可用
\usetikzlibrary{positioning,calc}

% docs/_common/latex/headerfooter.tex

\usepackage{fancyhdr}
\pagestyle{fancy}

\setlength{\headheight}{20pt}
\setlength{\headsep}{12pt}

% 左上角 LOGO 命令
\newcommand{\neowayheaderlogo}{%
  \includegraphics[height=14pt]{header-logo.png}
}

% 正常页面样式
\fancypagestyle{normal}{
    \fancyhf{}
    \fancyhead[L]{\neowayheaderlogo}
    \fancyhead[R]{\nouppercase{\leftmark}}
    \fancyfoot[L]{深圳市有方科技股份有限公司 版权所有}
    \fancyfoot[R]{\thepage}
    \renewcommand{\headrulewidth}{0.4pt}
    \renewcommand{\footrulewidth}{0.4pt}
}

% plain：用于 TOC / Chapter 起始页
\fancypagestyle{plain}{
    \fancyhf{}
    \fancyhead[L]{\neowayheaderlogo}
    \fancyhead[R]{}
    \fancyfoot[L]{深圳市有方科技股份有限公司 版权所有}
    \fancyfoot[R]{\thepage}
    \renewcommand{\headrulewidth}{0.4pt}
    \renewcommand{\footrulewidth}{0.4pt}
}

% 默认页式
\pagestyle{normal}

% ===== Neoway Patch: remove blank pages from openright =====
\makeatletter
\let\origcleardoublepage\cleardoublepage
\renewcommand{\cleardoublepage}{\clearpage}
\makeatother


% ===== Neoway Patch: force TOC to use headerfooter.tex plain style =====
\AtBeginDocument{
    \addtocontents{toc}{\protect\thispagestyle{plain}}
}
""",
    "maketitle": r"""% -------- Neoway 文档封面 --------
\thispagestyle{empty}
\pagenumbering{gobble}

\begin{titlepage}
  \begin{tikzpicture}[remember picture, overlay]
    \node[anchor=north west, inner sep=0pt] at (current page.north west)
      {\includegraphics[width=\paperwidth,height=\paperheight]{background.png}};
  \end{tikzpicture}

  \vspace*{8cm}
  \begin{flushleft}
    {\color[HTML]{70AD47}\fontsize{42}{48}\selectfont \textbf{ N706B }}
    \\[0.8cm]
    {\fontsize{28}{32}\selectfont AT\_Command\_Manual}
    \\[0.6cm]
    {\large 版本 V1.0 \hspace{1em} 日期 2025年11月15日}
  \end{flushleft}
\end{titlepage}

\clearpage
\pagenumbering{roman}""",
}

# <<< AUTO_LATEX_END
