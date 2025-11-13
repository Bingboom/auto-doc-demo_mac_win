import sys
from pathlib import Path

# 引入上级通用配置
sys.path.append(str(Path(__file__).resolve().parents[2] / "_common"))
from conf_common import *  # noqa

# 项目信息
project = 'Neoway N706B AT Command Manual'
author = 'Neoway Documentation Team'
version = 'v1.4'
release = version

# 通用 Sphinx 配置
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.githubpages',
    'sphinx.ext.todo',
]

templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

html_theme = 'alabaster'
html_static_path = ['_static']

# LaTeX 输出配置（引用全局 latex_elements）
latex_documents = [
    (master_doc, 'Neoway_N706B_Manual.tex', project, author, 'manual'),
]

# >>> BEGIN: NEOWAY_LATEX_BLOCK
# 自动注入时间：2025-11-13 12:16:56
if 'latex_elements' not in globals():
    latex_elements = {}
latex_engine = 'xelatex'
latex_additional_files = globals().get('latex_additional_files', []) + [
    '../../_common/_static/logo.png',
    '../../_common/_static/background.png',
    '../../_common/_static/header-logo.png',
]
latex_documents = [
    ('index', 'Neoway_N706B_Manual.tex', 'Neoway N706B AT 命令手册', 'Neoway 文档工程组', 'manual')
]
latex_elements.update({
    'papersize': 'a4paper',
    'pointsize': '11pt',
    'extraclassoptions': 'openany,oneside',
    'geometry': r'\usepackage[a4paper,top=22mm,bottom=22mm,left=22mm,right=22mm,headheight=24pt]{geometry}',
    'fontpkg': r'''
        \usepackage{xeCJK}
        \setCJKmainfont{PingFang SC}
        \setmainfont{Times New Roman}
        \setsansfont{Arial}
        \setmonofont{Menlo}
    ''',
    'preamble': r'''
        \usepackage{graphicx,tikz,eso-pic,xcolor,fancyhdr,titlesec,hyperref}
        \graphicspath{{./}{../../_common/_static/}{_common/_static/}}
        \setlength{\headheight}{24pt}
        \setlength{\headsep}{12pt}
        \hypersetup{
          pdftitle={ Neoway N706B AT 命令手册 },
          pdfauthor={ Neoway 文档工程组 },
          pdfsubject={ 深圳市有方科技股份有限公司 机密 | N706B | V1.4 },
          colorlinks=true, linkcolor=blue, urlcolor=blue
        }
        \newcommand{\neowayheaderlogo}{\includegraphics[scale=0.25]{header-logo.png}}
        \makeatletter
        % ---- 修复 chapter 标记，防止重复章节号 ----
        \renewcommand{\chaptermark}[1]{\markboth{#1}{}}
        \renewcommand{\sectionmark}[1]{\markright{#1}}
        \makeatother
        % ---- 页眉页脚样式 ----
        \fancypagestyle{normal}{%
          \fancyhf{}%
          \fancyhead[L]{\neowayheaderlogo}%
          \fancyhead[R]{第~\thechapter~章~\nouppercase{\leftmark}}%
          \fancyfoot[L]{深圳市有方科技股份有限公司版权所有}%
          \fancyfoot[R]{\thepage}%
          \renewcommand{\headrulewidth}{0.4pt}%
          \renewcommand{\footrulewidth}{0.4pt}%
        }
        \fancypagestyle{plain}{%
          \fancyhf{}%
          \fancyhead[L]{\neowayheaderlogo}%
          \fancyhead[R]{第~\thechapter~章~\nouppercase{\leftmark}}%
          \fancyfoot[L]{深圳市有方科技股份有限公司版权所有}%
          \fancyfoot[R]{\thepage}%
          \renewcommand{\headrulewidth}{0.4pt}%
          \renewcommand{\footrulewidth}{0.4pt}%
        }
        \let\cleardoublepage\clearpage
    ''',
    'maketitle': (
        r'''% -------- Neoway 封面 --------
\thispagestyle{empty}
\pagenumbering{gobble}
\begin{titlepage}
  \begin{tikzpicture}[remember picture, overlay]
    \node[anchor=north west, inner sep=0pt] at (current page.north west)
      {\includegraphics[width=\paperwidth,height=\paperheight]{_common/_static/background.png}};
  \end{tikzpicture}
  \vspace*{8cm}
  \begin{flushleft}
    {\color[HTML]{70AD47}\fontsize{42}{48}\selectfont \textbf{N706B}}\\[0.8cm]
    {\fontsize{28}{32}\selectfont AT 命令手册}\\[0.6cm]
    {\large 版本 V1.4 \hspace{1em} 日期 2025年11月13日}
  \end{flushleft}
\end{titlepage}
\clearpage
\pagenumbering{roman}
'''
    ),
})
# <<< END:  NEOWAY_LATEX_BLOCK

