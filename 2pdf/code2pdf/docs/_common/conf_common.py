# ================================================================
# 📘 Neoway Docs Common Config（共享基础配置）
#  统一跨项目的 Sphinx/LaTeX 公共配置
# ================================================================
from pathlib import Path
import os
import sys
import platform
from datetime import datetime

# === 路径定义 ===
COMMON_ROOT = Path(__file__).resolve().parent
COMMON_STATIC_PATH = COMMON_ROOT / "_static"

# 确保 _static 在路径中可访问
sys.path.insert(0, str(COMMON_ROOT))

# === 通用信息 ===
author = "Neoway 文档工程组"
copyright = f"{datetime.now().year}, Neoway Technology"
language = "zh_CN"

# === HTML 静态资源 ===
html_static_path = [str(COMMON_STATIC_PATH)]
html_logo = str(COMMON_STATIC_PATH / "logo.png")

# === LaTeX 资源路径（公共静态引用） ===
latex_engine = "xelatex"
latex_additional_files = [
    str(COMMON_STATIC_PATH / "logo.png"),
    str(COMMON_STATIC_PATH / "header-logo.png"),
    str(COMMON_STATIC_PATH / "background.png"),
]

# === 跨平台字体自动识别 ===
sys_name = platform.system().lower()
if "windows" in sys_name:
    zh_main, zh_sans, zh_mono = "SimSun", "SimHei", "FangSong"
    en_main, en_sans, en_mono = "Times New Roman", "Arial", "Consolas"
elif "darwin" in sys_name:  # macOS
    zh_main, zh_sans, zh_mono = "PingFang SC", "STHeiti", "PingFang SC"
    en_main, en_sans, en_mono = "Times New Roman", "Arial", "Menlo"
else:  # Linux
    zh_main, zh_sans, zh_mono = "Noto Sans CJK SC", "Noto Sans CJK SC", "Noto Sans Mono CJK SC"
    en_main, en_sans, en_mono = "Times New Roman", "Arial", "DejaVu Sans Mono"

# === 公共 LaTeX 元素（在各子 conf.py 里继承 update() 即可） ===
latex_elements = {
    'papersize': 'a4paper',
    'pointsize': '11pt',
    'extraclassoptions': 'openany,oneside',
    'geometry': r'\usepackage[a4paper,top=22mm,bottom=22mm,left=25mm,right=25mm,headheight=25pt]{geometry}',

    'fontpkg': rf'''
\usepackage{{xeCJK}}
\setCJKmainfont{{{zh_main}}}
\setCJKsansfont{{{zh_sans}}}
\setCJKmonofont{{{zh_mono}}}
\setmainfont{{{en_main}}}
\setsansfont{{{en_sans}}}
\setmonofont{{{en_mono}}}
\linespread{{1.3}}
''',

    'preamble': r'''
\usepackage{fancyhdr}
\usepackage{titlesec}
\usepackage{tocloft}
\usepackage{hyperref}
\usepackage{setspace}
\usepackage{graphicx}
\usepackage{xcolor}
\usepackage{tikz}

% ===== 页眉页脚 =====
\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{\includegraphics[scale=0.25]{../../_common/_static/header-logo.png}}
\fancyhead[R]{\leftmark}
\fancyfoot[L]{深圳市有方科技股份有限公司版权所有}
\fancyfoot[R]{\thepage}
\renewcommand{\headrulewidth}{0.4pt}
\renewcommand{\footrulewidth}{0.4pt}
\setlength{\headheight}{25pt}

% ===== 中文目录与章节 =====
\renewcommand{\contentsname}{\centering 目~录}
\titleformat{\chapter}{\Huge\bfseries}{第\,\thechapter\,章}{1em}{}
\let\cleardoublepage\clearpage
'''
}
