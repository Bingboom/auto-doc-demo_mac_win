# tools/latex_inject.py
# ================================================================
# 📘 Neoway LaTeX 样式注入 v3.3 — 企业稳定修正版
#    - 修复页眉“第1章 第1章”重复
#    - 支持 conf_common.py 全局常量
#    - 幂等注入 + 容错处理 + 平台字体适配
# ================================================================
from pathlib import Path
import re
from datetime import datetime

BEGIN_MARK = "# >>> BEGIN: NEOWAY_LATEX_BLOCK"
END_MARK   = "# <<< END:  NEOWAY_LATEX_BLOCK"


def inject_latex_block(conf_path: Path, title: str, author: str, model_name: str,
                       version: str, doc_type: str = "AT 命令手册",
                       subject_prefix: str = "Neoway 机密") -> None:
    """向 conf.py 注入 LaTeX 样式块"""
    conf_path = Path(conf_path)
    if not conf_path.exists():
        raise FileNotFoundError(f"conf.py 未找到：{conf_path}")

    version_tag = "V" + version.lstrip("vV")
    subject = f"{subject_prefix} | {model_name} | {version_tag}"

    # === 封面区 ===
    cover_block = (
        r"% -------- Neoway 封面 --------"+"\n"
        r"\thispagestyle{empty}"+"\n"
        r"\pagenumbering{gobble}"+"\n"
        r"\begin{titlepage}"+"\n"
        r"  \begin{tikzpicture}[remember picture, overlay]"+"\n"
        r"    \node[anchor=north west, inner sep=0pt] at (current page.north west)"
        r"      {\includegraphics[width=\paperwidth,height=\paperheight]{_common/_static/background.png}};"+"\n"
        r"  \end{tikzpicture}"+"\n"
        r"  \vspace*{8cm}"+"\n"
        r"  \begin{flushleft}"+"\n"
        r"    {\color[HTML]{70AD47}\fontsize{42}{48}\selectfont \textbf{" + model_name + r"}}\\[0.8cm]"+"\n"
        r"    {\fontsize{28}{32}\selectfont " + doc_type + r"}\\[0.6cm]"+"\n"
        r"    {\large 版本 " + version_tag + r" \hspace{1em} 日期 " + datetime.now().strftime("%Y年%m月%d日") + r"}"+"\n"
        r"  \end{flushleft}"+"\n"
        r"\end{titlepage}"+"\n"
        r"\clearpage"+"\n"
        r"\pagenumbering{roman}"+"\n"
    )

    # === 核心注入块 ===
    latex_block = (
        BEGIN_MARK + "\n"
        + f"# 自动注入时间：{datetime.now():%Y-%m-%d %H:%M:%S}\n"
        + "if 'latex_elements' not in globals():\n"
        + "    latex_elements = {}\n"
        + "latex_engine = 'xelatex'\n"
        + "latex_additional_files = globals().get('latex_additional_files', []) + [\n"
        + "    '../../_common/_static/logo.png',\n"
        + "    '../../_common/_static/background.png',\n"
        + "    '../../_common/_static/header-logo.png',\n"
        + "]\n"
        + "latex_documents = [\n"
        + f"    ('index', 'Neoway_{model_name}_Manual.tex', '{title}', '{author}', 'manual')\n"
        + "]\n"
        + "latex_elements.update({\n"
        + "    'papersize': 'a4paper',\n"
        + "    'pointsize': '11pt',\n"
        + "    'extraclassoptions': 'openany,oneside',\n"
        + "    'geometry': r'\\usepackage[a4paper,top=22mm,bottom=22mm,left=22mm,right=22mm,headheight=24pt]{geometry}',\n"
        + "    'fontpkg': r'''\n"
        + "        \\usepackage{xeCJK}\n"
        + "        \\setCJKmainfont{PingFang SC}\n"
        + "        \\setmainfont{Times New Roman}\n"
        + "        \\setsansfont{Arial}\n"
        + "        \\setmonofont{Menlo}\n"
        + "    ''',\n"
        + "    'preamble': r'''\n"
        + "        \\usepackage{graphicx,tikz,eso-pic,xcolor,fancyhdr,titlesec,hyperref}\n"
        + "        \\graphicspath{{./}{../../_common/_static/}{_common/_static/}}\n"
        + "        \\setlength{\\headheight}{24pt}\n"
        + "        \\setlength{\\headsep}{12pt}\n"
        + "        \\hypersetup{\n"
        + "          pdftitle={" + title + "},\n"
        + "          pdfauthor={" + author + "},\n"
        + "          pdfsubject={" + subject + "},\n"
        + "          colorlinks=true, linkcolor=blue, urlcolor=blue\n"
        + "        }\n"
        + "        \\newcommand{\\neowayheaderlogo}{\\includegraphics[scale=0.25]{header-logo.png}}\n"
        + "        \\makeatletter\n"
        + "        % ---- 修复 chapter 标记，防止重复章节号 ----\n"
        + "        \\renewcommand{\\chaptermark}[1]{\\markboth{#1}{}}\n"
        + "        \\renewcommand{\\sectionmark}[1]{\\markright{#1}}\n"
        + "        \\makeatother\n"
        + "        % ---- 页眉页脚样式 ----\n"
        + "        \\fancypagestyle{normal}{%\n"
        + "          \\fancyhf{}%\n"
        + "          \\fancyhead[L]{\\neowayheaderlogo}%\n"
        + "          \\fancyhead[R]{第~\\thechapter~章~\\nouppercase{\\leftmark}}%\n"
        + "          \\fancyfoot[L]{深圳市有方科技股份有限公司版权所有}%\n"
        + "          \\fancyfoot[R]{\\thepage}%\n"
        + "          \\renewcommand{\\headrulewidth}{0.4pt}%\n"
        + "          \\renewcommand{\\footrulewidth}{0.4pt}%\n"
        + "        }\n"
        + "        \\fancypagestyle{plain}{%\n"
        + "          \\fancyhf{}%\n"
        + "          \\fancyhead[L]{\\neowayheaderlogo}%\n"
        + "          \\fancyhead[R]{第~\\thechapter~章~\\nouppercase{\\leftmark}}%\n"
        + "          \\fancyfoot[L]{深圳市有方科技股份有限公司版权所有}%\n"
        + "          \\fancyfoot[R]{\\thepage}%\n"
        + "          \\renewcommand{\\headrulewidth}{0.4pt}%\n"
        + "          \\renewcommand{\\footrulewidth}{0.4pt}%\n"
        + "        }\n"
        + "        \\let\\cleardoublepage\\clearpage\n"
        + "    ''',\n"
        + "    'maketitle': (\n"
        + "        r'''"
        + cover_block +
        "'''\n"
        + "    ),\n"
        + "})\n"
        + END_MARK + "\n"
    )

    # === 写入操作 ===
    txt = conf_path.read_text(encoding="utf-8")
    txt = re.sub(rf"{re.escape(BEGIN_MARK)}.*?{re.escape(END_MARK)}", "", txt, flags=re.DOTALL).rstrip() + "\n\n"
    conf_path.write_text(txt + latex_block, encoding="utf-8")
    print(f"✅ 已注入 LaTeX 样式块 → {conf_path}")
