# ================================================================
# 📘 Neoway Build PDF v7.7 — 最终版：封面路径修复 + LaTeX缓存清理 + 字体安全
# ================================================================
import os, re, shutil, subprocess, platform, sys
from pathlib import Path
from datetime import datetime

# ✅ 确保能导入 tools 内的模块
CURRENT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CURRENT_DIR.parent
sys.path.insert(0, str(PROJECT_ROOT))

# ✅ 导入 CSV → RST 构建脚本
from tools.render_rst import *

# === 基础信息 ===
LANG = "zh"
MODEL_NAME = "N706B"
VERSION = "v1.4"

DOC_TYPE_CN = "AT 命令手册"
AUTHOR_CN = "Neoway 文档工程组"

DATE = datetime.now()
DATE_CN = DATE.strftime("%Y年%m月%d日")
VERSION_TAG = VERSION.strip().replace("v", "V")

# === 语言选择 ===
DOC_TYPE = DOC_TYPE_CN
AUTHOR = AUTHOR_CN
DATE_SHOW = DATE_CN
TITLE = f"Neoway {MODEL_NAME} {DOC_TYPE_CN}"
SUBJECT = f"Neoway 机密 | {MODEL_NAME} | {VERSION_TAG}"

# === 路径定位 ===
PROJECT_ROOT = Path.cwd()
for p in [PROJECT_ROOT] + list(PROJECT_ROOT.parents):
    if (p / "docs" / MODEL_NAME / "source" / "conf.py").exists():
        PROJECT_ROOT = p
        break
else:
    raise FileNotFoundError("❌ 未找到 conf.py，请确认 docs/{MODEL_NAME}/source 目录结构正确。")

ROOT_DIR = PROJECT_ROOT / "docs" / MODEL_NAME / "source"
BUILD_DIR = PROJECT_ROOT / "docs" / MODEL_NAME / "build"
LATEX_DIR = BUILD_DIR / "latex"
PDF_DIR = BUILD_DIR / "pdf"
PDF_DIR.mkdir(parents=True, exist_ok=True)
conf_path = ROOT_DIR / "conf.py"

# ✅ 构建前清理旧 LaTeX 文件，防止缓存导致空白页
if LATEX_DIR.exists():
    shutil.rmtree(LATEX_DIR)
    print("🧹 已清理旧的 LaTeX 构建目录。")

# ✅ 自动生成 RST 步骤
print("🧩 生成 RST 文件中（CSV → RST）...")
subprocess.run(["python", "tools/render_rst.py"], check=True)
print("✅ RST 生成完成，准备构建 PDF。")

# === 平台字体选择 ===
sys_name = platform.system().lower()
if "darwin" in sys_name or "mac" in sys_name:
    zh_font = "PingFang SC"
    mono_font = "Menlo"
elif "win" in sys_name:
    zh_font = "Microsoft YaHei"
    mono_font = "Consolas"
else:
    zh_font = "Noto Sans CJK SC"
    mono_font = "DejaVu Sans Mono"

# === 拷贝背景图到 LaTeX 输出目录，确保路径可见 ===
bg_src = PROJECT_ROOT / "docs" / "_common" / "_static" / "background.png"
bg_dst = LATEX_DIR / "background.png"
bg_dst.parent.mkdir(parents=True, exist_ok=True)
if bg_src.exists():
    shutil.copy2(bg_src, bg_dst)
    print(f"✅ 已复制背景图到 {bg_dst}")
else:
    print(f"⚠️ 警告：未找到背景图 {bg_src}")

# === 封面模板 ===
cover_block = rf"""
%% -------- Neoway 封面 --------
\thispagestyle{{empty}}
\pagenumbering{{gobble}}
\begin{{titlepage}}
  \begin{{tikzpicture}}[remember picture, overlay]
    \node[anchor=north west, inner sep=0pt] at (current page.north west)
      {{\includegraphics[width=\paperwidth,height=\paperheight]{{background.png}}}};
  \end{{tikzpicture}}
  \vspace*{{8cm}}
  \begin{{flushleft}}
    {{\color[HTML]{{70AD47}}\fontsize{{42}}{{48}}\selectfont \textbf{{{MODEL_NAME}}}}}\\[0.8cm]
    {{\fontsize{{28}}{{32}}\selectfont {DOC_TYPE}}}\\[0.6cm]
    {{\large 版本 {VERSION_TAG} \hspace{{1em}} 日期 {DATE_SHOW}}}
  \end{{flushleft}}
\end{{titlepage}}
\clearpage
\pagenumbering{{roman}}
"""

# === 注入标记 ===
marker_begin = "# >>> BEGIN: NEOWAY_LATEX_BLOCK"
marker_end   = "# <<< END:  NEOWAY_LATEX_BLOCK"

conf_txt = conf_path.read_text(encoding="utf-8")
conf_txt = re.sub(rf"{re.escape(marker_begin)}.*?{re.escape(marker_end)}", "", conf_txt, flags=re.DOTALL)

latex_block = f"""{marker_begin}
# 自动注入时间：{datetime.now():%Y-%m-%d %H:%M:%S}
latex_engine = 'xelatex'
latex_additional_files = [
    '../../_common/_static/logo.png',
    '../../_common/_static/header-logo.png',
    'background.png'
]
latex_documents = [('index', 'Neoway_{MODEL_NAME}_Manual.tex', '{TITLE}', '{AUTHOR}', 'manual')]

latex_elements = globals().get('latex_elements', {{}})

latex_elements.update({{
    'papersize': 'a4paper',
    'pointsize': '11pt',
    'extraclassoptions': 'openany,oneside',
    'geometry': r'\\usepackage[a4paper,top=22mm,bottom=22mm,left=22mm,right=22mm,headheight=25pt]{{geometry}}',
    'fontpkg': r'''
\\usepackage{{xeCJK}}
\\setCJKmainfont{{{zh_font}}}
\\setmainfont{{Times New Roman}}
\\setsansfont{{Arial}}
\\setmonofont{{{mono_font}}}
    ''',
    'preamble': r'''
\\usepackage{{graphicx,tikz,eso-pic,xcolor,fancyhdr,titlesec,hyperref}}
\\graphicspath{{{{./}}{{../../_common/_static/}}{{../../../_common/_static/}}}}
\\setlength{{\\headheight}}{{25pt}}
\\setlength{{\\headsep}}{{12pt}}

\\hypersetup{{
  pdftitle={{ {TITLE} }},
  pdfauthor={{ {AUTHOR} }},
  pdfsubject={{ {SUBJECT} }},
  colorlinks=true, linkcolor=blue, urlcolor=blue
}}

\\newcommand{{\\neowayheaderlogo}}{{\\includegraphics[scale=0.25]{{header-logo.png}}}}
\\makeatletter
\\renewcommand{{\\chaptermark}}[1]{{\\markboth{{#1}}{{}}}}
\\renewcommand{{\\sectionmark}}[1]{{\\markright{{#1}}}}
\\makeatother

\\fancypagestyle{{normal}}{{%
  \\fancyhf{{}}%
  \\fancyhead[L]{{\\neowayheaderlogo}}%
  \\fancyhead[R]{{\\nouppercase{{\\rightmark}}}}%
  \\fancyfoot[L]{{深圳市有方科技股份有限公司版权所有}}%
  \\fancyfoot[R]{{\\thepage}}%
  \\renewcommand{{\\headrulewidth}}{{0.4pt}}%
  \\renewcommand{{\\footrulewidth}}{{0.4pt}}%
}}

\\fancypagestyle{{plain}}{{%
  \\fancyhf{{}}%
  \\fancyhead[L]{{\\neowayheaderlogo}}%
  \\fancyhead[R]{{\\nouppercase{{\\rightmark}}}}%
  \\fancyfoot[L]{{深圳市有方科技股份有限公司版权所有}}%
  \\fancyfoot[R]{{\\thepage}}%
  \\renewcommand{{\\headrulewidth}}{{0.4pt}}%
  \\renewcommand{{\\footrulewidth}}{{0.4pt}}%
}}
    \\let\\cleardoublepage\\clearpage
    ''',
    'maketitle': r\"\"\"{cover_block}\"\"\",\n}})\n{marker_end}
"""

conf_path.write_text(conf_txt.rstrip() + "\n\n" + latex_block + "\n", encoding="utf-8")
print(f"✅ 已更新 {conf_path}（{LANG.upper()} 版封面 + 页眉LOGO）")

# === 构建 Sphinx LaTeX ===
subprocess.run(["sphinx-build", "-b", "latex", str(ROOT_DIR), str(LATEX_DIR)], check=True)

# === 同步公共资源 ===
common_static = PROJECT_ROOT / "docs" / "_common" / "_static"
dest_common = LATEX_DIR / "_common" / "_static"
if common_static.exists():
    shutil.copytree(common_static, dest_common, dirs_exist_ok=True)
    print(f"✅ 已复制公共资源到 {dest_common}")

os.chdir(LATEX_DIR)
tex_main = next(LATEX_DIR.glob("*.tex"))

# === 编译两轮 XeLaTeX ===
for i in range(2):
    print(f"🌀 XeLaTeX 第 {i+1}/2 轮 …")
    subprocess.run(["xelatex", "-interaction=nonstopmode", tex_main.name], check=True)

# === 输出 PDF 命名 ===
version_label = VERSION_TAG.lstrip("Vv")
output_filename = f"Neoway_{MODEL_NAME}_{DOC_TYPE}_V{version_label}.pdf".replace(" ", "_")
out_pdf = PDF_DIR / output_filename

pdfs = sorted(LATEX_DIR.glob("*.pdf"), key=lambda p: p.stat().st_mtime, reverse=True)
if pdfs:
    shutil.copy2(pdfs[0], out_pdf)
    print(f"🎉 成功生成 PDF：{out_pdf}")
else:
    print("❌ 未生成 PDF，请检查 LaTeX 日志。")
