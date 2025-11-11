# -*- coding: utf-8 -*-
# ================================================================
# 📘 Neoway Latex Inject v3.6 — 企业集成版（UTF-8 +BOM）
# ================================================================
# 功能说明：
# 1️⃣ 自动向 docs/<MODEL>/source/conf.py 注入 LaTeX 样式。
# 2️⃣ 支持公司信息、字体、封面、页眉页脚的统一管理。
# 3️⃣ 向后兼容旧版 build_pdf.py 调用（不传 company 参数也可）。
# 4️⃣ 可跨平台（Windows/macOS/Linux）使用。
# ---------------------------------------------------------------
# 最近更新：
# - 新增 company / zh_font / mono_font / date_cn 参数。
# - 修复章节页眉错位问题。
# - 支持多项目复用（不同型号同模板）。
# ================================================================

from datetime import datetime
from pathlib import Path
import re


def inject_latex_block(
    conf_path: Path,
    model_name: str,
    version: str,
    doc_type: str,
    author: str,
    company: str = "Neoway Technology",
    zh_font: str = "PingFang SC",
    mono_font: str = "Menlo",
    date_cn: str = None,
):
    """
    自动向 conf.py 注入 LaTeX 样式块。
    参数：
      conf_path  - conf.py 路径
      model_name - 模块型号（如 N706B）
      version    - 文档版本号（如 v1.4）
      doc_type   - 文档类型（如 AT 命令手册）
      author     - 作者（如 Neoway 文档工程组）
      company    - 公司名（默认 Neoway Technology）
      zh_font    - 中文字体（默认 PingFang SC）
      mono_font  - 等宽字体（默认 Menlo）
      date_cn    - 中文日期字符串（默认自动生成）
    """
    if not conf_path.exists():
        raise FileNotFoundError(f"❌ 找不到 conf.py：{conf_path}")

    date_cn = date_cn or datetime.now().strftime("%Y年%m月%d日")
    version_tag = ("V" + version.lstrip("vV")).strip()
    title = f"Neoway {model_name} {doc_type}"
    subject = f"{company} 机密 | {model_name} | {version_tag}"

    # === 标记区间定义 ===
    marker_begin = "# >>> BEGIN: NEOWAY_LATEX_BLOCK"
    marker_end = "# <<< END:  NEOWAY_LATEX_BLOCK"

    conf_txt = conf_path.read_text(encoding="utf-8")

    # === 删除旧版本注入内容 ===
    conf_txt = re.sub(
        rf"{re.escape(marker_begin)}.*?{re.escape(marker_end)}",
        "",
        conf_txt,
        flags=re.DOTALL,
    )

    # === 构建新的 LaTeX 注入块 ===
    block = f"""{marker_begin}
# 自动注入时间：{datetime.now():%Y-%m-%d %H:%M:%S}
if 'latex_elements' not in globals():
    latex_elements = {{}}
latex_engine = 'xelatex'
latex_additional_files = globals().get('latex_additional_files', []) + [
    '../../_common/_static/logo.png',
    '../../_common/_static/background.png',
    '../../_common/_static/header-logo.png',
]
latex_documents = [
    ('index', 'Neoway_{model_name}_Manual.tex', '{title}', '{author}', 'manual')
]
latex_elements.update({{
    'papersize': 'a4paper',
    'pointsize': '11pt',
    'extraclassoptions': 'openany,oneside',
    'geometry': r'\\usepackage[a4paper,top=22mm,bottom=22mm,left=22mm,right=22mm,headheight=24pt]{{geometry}}',
    'fontpkg': r'''
        \\usepackage{{xeCJK}}
        \\setCJKmainfont{{{zh_font}}}
        \\setmainfont{{Times New Roman}}
        \\setsansfont{{Arial}}
        \\setmonofont{{{mono_font}}}
    ''',
    'preamble': r'''
        \\usepackage{{graphicx,tikz,eso-pic,xcolor,fancyhdr,titlesec,hyperref}}
        \\graphicspath{{{{./}}{{../../_common/_static/}}{{_common/_static/}}}}
        \\setlength{{\\headheight}}{{24pt}}
        \\setlength{{\\headsep}}{{12pt}}
        \\hypersetup{{
          pdftitle={{ {title} }},
          pdfauthor={{ {author} }},
          pdfsubject={{ {subject} }},
          colorlinks=true, linkcolor=blue, urlcolor=blue
        }}
        \\newcommand{{\\neowayheaderlogo}}{{\\includegraphics[scale=0.25]{{header-logo.png}}}}
        \\makeatletter
        % ---- 修复 chapter 标记，防止重复章节号 ----
        \\renewcommand{{\\chaptermark}}[1]{{\\markboth{{#1}}{{}}}}
        \\renewcommand{{\\sectionmark}}[1]{{\\markright{{#1}}}}
        \\makeatother
        % ---- 页眉页脚样式 ----
        \\fancypagestyle{{normal}}{{%
          \\fancyhf{{}}%
          \\fancyhead[L]{{\\neowayheaderlogo}}%
          \\fancyhead[R]{{第~\\thechapter~章~\\nouppercase{{\\leftmark}}}}%
          \\fancyfoot[L]{{{company}版权所有}}%
          \\fancyfoot[R]{{\\thepage}}%
          \\renewcommand{{\\headrulewidth}}{{0.4pt}}%
          \\renewcommand{{\\footrulewidth}}{{0.4pt}}%
        }}
        \\fancypagestyle{{plain}}{{%
          \\fancyhf{{}}%
          \\fancyhead[L]{{\\neowayheaderlogo}}%
          \\fancyhead[R]{{第~\\thechapter~章~\\nouppercase{{\\leftmark}}}}%
          \\fancyfoot[L]{{{company}版权所有}}%
          \\fancyfoot[R]{{\\thepage}}%
          \\renewcommand{{\\headrulewidth}}{{0.4pt}}%
          \\renewcommand{{\\footrulewidth}}{{0.4pt}}%
        }}
        \\let\\cleardoublepage\\clearpage
    ''',
    'maketitle': (
        r'''% -------- Neoway 封面 --------
\\thispagestyle{{empty}}
\\pagenumbering{{gobble}}
\\begin{{titlepage}}
  \\begin{{tikzpicture}}[remember picture, overlay]
    \\node[anchor=north west, inner sep=0pt] at (current page.north west)
      {{\\includegraphics[width=\\paperwidth,height=\\paperheight]{{_common/_static/background.png}}}};
  \\end{{tikzpicture}}
  \\vspace*{{8cm}}
  \\begin{{flushleft}}
    {{\\color[HTML]{{70AD47}}\\fontsize{{42}}{{48}}\\selectfont \\textbf{{{model_name}}}}}\\\\[0.8cm]
    {{\\fontsize{{28}}{{32}}\\selectfont {doc_type}}}\\\\[0.6cm]
    {{\\large 版本 {version_tag} \\hspace{{1em}} 日期 {date_cn}}}
  \\end{{flushleft}}
\\end{{titlepage}}
\\clearpage
\\pagenumbering{{roman}}
'''
    ),
}})
{marker_end}
"""
    conf_txt = conf_txt.rstrip() + "\n\n" + block + "\n"
    conf_path.write_text(conf_txt, encoding="utf-8-sig")  # UTF-8 +BOM
    print(f"✅ 已更新 {conf_path}")
