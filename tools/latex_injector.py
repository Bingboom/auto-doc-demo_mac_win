# tools/latex_injector.py
import re
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def inject_latex_block(conf_path: Path, model_name: str, version: str, doc_type: str, author: str, styles: dict):

    tex_filename = f"Neoway_{model_name}_Manual.tex"
    title = f"Neoway {model_name} {doc_type}"

    conf_text = conf_path.read_text(encoding="utf-8")

    marker_begin = "# >>> AUTO_LATEX_BEGIN"
    marker_end = "# <<< AUTO_LATEX_END"

    conf_text = re.sub(
        rf"{re.escape(marker_begin)}.*?{re.escape(marker_end)}",
        "",
        conf_text,
        flags=re.DOTALL
    )

    # ===== 移除 openright blank page =====
    remove_openright_blank_patch = r"""
% ===== Neoway Patch: remove blank pages from openright =====
\makeatletter
\let\origcleardoublepage\cleardoublepage
\renewcommand{\cleardoublepage}{\clearpage}
\makeatother
"""

    # ===== TOC 使用用户 headerfooter.tex 内定义的 plain 样式 =====
    fix_toc_header_patch = r"""
% ===== Neoway Patch: force TOC to use headerfooter.tex plain style =====
\AtBeginDocument{
    \addtocontents{toc}{\protect\thispagestyle{plain}}
}
"""

    patched_preamble = (
        styles["preamble_full"].rstrip()
        + "\n"
        + remove_openright_blank_patch
        + "\n"
        + fix_toc_header_patch
    )

    block = f"""
{marker_begin}

latex_engine = "xelatex"

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
    print(f"✔ 已注入 LaTeX 样式（headerfooter 完全接管）: {conf_path}")
