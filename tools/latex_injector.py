# tools/latex_injector.py
import re
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def inject_latex_block(conf_path: Path, model_name: str, version: str, doc_type: str, author: str, styles: dict):

    # ==== 构建生成的 tex 文件名 ====
    tex_filename = f"Neoway_{model_name}_Manual.tex"
    title = f"Neoway {model_name} {doc_type}"

    # 读取 conf.py
    conf_text = conf_path.read_text(encoding="utf-8")

    marker_begin = "# >>> AUTO_LATEX_BEGIN"
    marker_end = "# <<< AUTO_LATEX_END"

    # 删除旧 block
    conf_text = re.sub(
        rf"{re.escape(marker_begin)}.*?{re.escape(marker_end)}",
        "",
        conf_text,
        flags=re.DOTALL
    )

    # ============= 关键补丁：干掉 openright 产生的空白页 =============
    remove_openright_blank_patch = r"""
% ===== Neoway patch: remove blank pages from openright/cleardoublepage =====
\makeatletter
\let\origcleardoublepage\cleardoublepage
\renewcommand{\cleardoublepage}{\clearpage}
\makeatother
"""

    # ============= 关键补丁：彻底修复 TOC 页眉 =============
    # Sphinx 对目录页（TOC）强制使用 \pagestyle{plain}，因此必须重写 plain 样式
    # 并且强制目录页执行 thispagestyle{plain}
    fix_toc_header_patch = r"""
% ===== Neoway patch: FIX TOC HEADER =====
% 强制重写 plain 样式（Sphinx 目录页默认使用 plain）
\fancypagestyle{plain}{
    \fancyhf{}
    % 左侧 logo（你在 latex_styles.py 中定义的）
    \fancyhead[L]{\neowayheaderlogo}
    % 右侧空白
    \fancyhead[R]{}
    \renewcommand{\headrulewidth}{0.4pt}
}

% 强制目录页使用 plain（覆盖 Sphinx 自动行为）
\AtBeginDocument{
    \addtocontents{toc}{\protect\thispagestyle{plain}}
}
"""

    # 合并 preamble
    patched_preamble = (
        styles["preamble_full"].rstrip()
        + "\n"
        + remove_openright_blank_patch
        + "\n"
        + fix_toc_header_patch
    )

    # 注入 block
    block = f"""
{marker_begin}

latex_engine = "xelatex"

# 生成 LaTeX 主文件名
latex_documents = [
    ('index', '{tex_filename}', '{title}', '{author}', 'manual')
]

latex_elements = {{
    "fontpkg": r\"\"\"{styles['fontpkg']}\"\"\",
    "preamble": r\"\"\"{patched_preamble}\"\"\",
    "maketitle": r\"\"\"{styles['cover']}\"\"\",
}}

{marker_end}
"""

    conf_path.write_text(conf_text.rstrip() + "\n\n" + block, encoding="utf-8")
    print(f"✔ 已注入 LaTeX 样式（含 TOC 页眉修复）：{conf_path}")
