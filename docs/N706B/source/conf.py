latex_elements = {
    "fontpkg": r"""% ===== LaTeX 字体统一配置 =====
\usepackage{xeCJK}
\setCJKmainfont{PingFang SC}
\setCJKsansfont{PingFang SC}
\setCJKmonofont{PingFang SC}

\setmainfont{Times New Roman}
\setsansfont{Arial}
\setmonofont{Menlo}
""",
    "preamble": r"""% docs/_common/latex/base_preamble.tex
\usepackage{graphicx}
\usepackage{tikz}
\usepackage{eso-pic}
\usepackage{xcolor}
\usepackage{fancyhdr}
\usepackage{titlesec}
\usepackage{hyperref}
\usepackage[a4paper, left=1in, right=1in, top=1in, bottom=1in]{geometry}

% 页眉页脚设置
\setlength{\headheight}{24pt}
\setlength{\headsep}{12pt}

\hypersetup{
  colorlinks=true,
  linkcolor=blue,
  urlcolor=blue,
  citecolor=blue,
  pdfborder={0 0 0}
}

\usetikzlibrary{positioning,calc}

% 设置背景图和封面样式
\usepackage{fancyhdr}
\pagestyle{fancy}

\setlength{\headheight}{20pt}
\setlength{\headsep}{12pt}


""",
    "maketitle": r"""% -------- Neoway 文档封面 --------
\thispagestyle{empty}
\pagenumbering{gobble}

\begin{titlepage}
  \begin{tikzpicture}[remember picture, overlay]
    \node[anchor=north west, inner sep=0pt] at (current page.north west)
      {\includegraphics[width=\paperwidth,height=\paperheight]{background.png}};
  \end{tikzpicture}
\clearpage
\pagenumbering{roman}
""",
}


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

  % 控制顶部间距
  \vspace*{6cm}  % 根据需要微调顶部间距

  % 使用 hspace* 来强制将 N706B 向左对齐
  \begin{flushleft}
    \hspace*{-0.4cm}  % 强制水平向左偏移
    {\color[HTML]{70AD47}\fontsize{42}{48}\selectfont \textbf{ N706B }} % 修改字体
    \vskip 0.8cm  % 控制标题和副标题之间的垂直间距

    {\fontsize{28}{32}\selectfont AT Commands Manual}
    \vskip 0.5cm  % 控制标题和日期之间的垂直间距

    {\large Issue 1.2 \hspace{1em} Date 2025-08-13}
  \end{flushleft}
\end{titlepage}

\clearpage
\pagenumbering{roman}""",
}

# <<< AUTO_LATEX_END
