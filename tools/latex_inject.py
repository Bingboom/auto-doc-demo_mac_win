# ================================================================
# 📘 Neoway LaTeX Inject v2.1 — 稳定可执行版（修复 SyntaxError）
# ================================================================
from datetime import datetime
import re

def inject_latex_block(conf_path, title, author, model_name, version):
    """向 conf.py 注入完整 LaTeX 块（含页眉章号+章节名）"""

    marker_begin = "# >>> BEGIN: NEOWAY_LATEX_BLOCK"
    marker_end   = "# <<< END:  NEOWAY_LATEX_BLOCK"

    # 封面模板
    cover_block = rf"""
% -------- Neoway 封面 --------
\thispagestyle{{empty}}
\pagenumbering{{gobble}}
\begin{{titlepage}}
  \begin{{tikzpicture}}[remember picture, overlay]
    \node[anchor=north west, inner sep=0pt] at (current page.north west)
      {{\includegraphics[width=\paperwidth,height=\paperheight]{{_common/_static/background.png}}}};
  \end{{tikzpicture}}
  \vspace*{{8cm}}
  \begin{{flushleft}}
    {{\color[HTML]{{70AD47}}\fontsize{{42}}{{48}}\selectfont \textbf{{{model_name}}}}}\\[0.8cm]
    {{\fontsize{{28}}{{32}}\selectfont AT 命令手册}}\\[0.6cm]
    {{\large 版本 {version} \hspace{{1em}} 日期 {datetime.now():%Y年%m月%d日}}}
  \end{{flushleft}}
\end{{titlepage}}
\clearpage
\pagenumbering{{roman}}
"""

    # LaTeX 注入区块
    latex_block = (
f"""{marker_begin}
# 自动注入时间：{datetime.now():%Y-%m-%d %H:%M:%S}
latex_engine = 'xelatex'
latex_additional_files = [
    '../../_common/_static/logo.png',
    '../../_common/_static/background.png',
    '../../_common/_static/header-logo.png'
]
latex_documents = [
    ('index', 'Neoway_{model_name}_Manual.tex', '{title}', '{author}', 'manual')
]
latex_elements = globals().get('latex_elements', {{}})
latex_elements.update({{
    'papersize': 'a4paper',
    'pointsize': '11pt',
    'extraclassoptions': 'openany,oneside',
    'geometry': r'\\usepackage[a4paper,top=22mm,bottom=22mm,left=22mm,right=22mm,headheight=18pt]{{geometry}}',

    'fontpkg': r'''
\\usepackage{{xeCJK}}
\\setCJKmainfont{{PingFang SC}}
\\setmainfont{{Times New Roman}}
\\setsansfont{{Arial}}
\\setmonofont{{Menlo}}
    ''',

    'preamble': r'''
\\usepackage{{graphicx,tikz,eso-pic,xcolor,fancyhdr,titlesec,hyperref}}
\\graphicspath{{{{./}}{{../../_common/_static/}}{{_common/_static/}}}}
\\setlength{{\\headheight}}{{24pt}}
\\setlength{{\\headsep}}{{12pt}}

\\hypersetup{{
  pdftitle={{ {title} }},
  pdfauthor={{ {author} }},
  colorlinks=true, linkcolor=blue, urlcolor=blue
}}

\\makeatletter
\\renewcommand{{\\chaptermark}}[1]{{\\markboth{{#1}}{{}}}}
\\renewcommand{{\\sectionmark}}[1]{{\\markright{{#1}}}}
\\makeatother

\\newcommand{{\\neowayheaderlogo}}{{\\includegraphics[scale=0.25]{{header-logo.png}}}}

\\fancypagestyle{{normal}}{{%
  \\fancyhf{{}}%
  \\fancyhead[L]{{\\neowayheaderlogo}}%
  \\fancyhead[R]{{\\nouppercase{{\\chaptername~\\thechapter~\\leftmark}}}}%
  \\fancyfoot[L]{{深圳市有方科技股份有限公司版权所有}}%
  \\fancyfoot[R]{{\\thepage}}%
  \\renewcommand{{\\headrulewidth}}{{0.4pt}}%
  \\renewcommand{{\\footrulewidth}}{{0.4pt}}%
}}

\\fancypagestyle{{plain}}{{%
  \\fancyhf{{}}%
  \\fancyhead[L]{{\\neowayheaderlogo}}%
  \\fancyhead[R]{{\\nouppercase{{\\chaptername~\\thechapter~\\leftmark}}}}%
  \\fancyfoot[L]{{深圳市有方科技股份有限公司版权所有}}%
  \\fancyfoot[R]{{\\thepage}}%
  \\renewcommand{{\\headrulewidth}}{{0.4pt}}%
  \\renewcommand{{\\footrulewidth}}{{0.4pt}}%
}}
\\let\\cleardoublepage\\clearpage
\\AtBeginDocument{{\\pagestyle{{normal}}}}
    ''',

    'maketitle': r'''{cover_block}''',
}})
{marker_end}
""")

    # 写入 conf.py
    txt = conf_path.read_text(encoding="utf-8")
    txt = re.sub(rf"{marker_begin}.*?{marker_end}", "", txt, flags=re.DOTALL)
    conf_path.write_text(txt.rstrip() + "\n\n" + latex_block + "\n", encoding="utf-8")
    print(f"✅ 已注入章节页眉与封面到 {conf_path}")
