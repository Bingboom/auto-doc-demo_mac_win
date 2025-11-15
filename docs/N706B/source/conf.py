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

