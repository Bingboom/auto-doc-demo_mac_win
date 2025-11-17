# tools/latex_injector.py
import re
from pathlib import Path

from utils.path_utils import latex_common_path

LATEX_DIR = latex_common_path()

def inject_latex_block(conf_path: Path, model: str, version: str, doc_type: str, author: str, styles: dict):

    tex_filename = f"Neoway_{model}_Manual.tex"
    title = f"Neoway {model} {doc_type}"

    conf_text = conf_path.read_text(encoding="utf-8")

    begin = "# >>> AUTO_LATEX_BEGIN"
    end = "# <<< AUTO_LATEX_END"

    conf_text = re.sub(
        rf"{re.escape(begin)}.*?{re.escape(end)}",
        "",
        conf_text,
        flags=re.DOTALL
    )

    remove_blank_pages = r"""
\makeatletter
\let\origcleardoublepage\cleardoublepage
\renewcommand{\cleardoublepage}{\clearpage}
\makeatother
"""

    force_plain_toc = r"""
\AtBeginDocument{
    \addtocontents{toc}{\protect\thispagestyle{plain}}
}
"""

    preamble_full = styles["preamble_full"] + "\n" + remove_blank_pages + "\n" + force_plain_toc

    block = f"""
{begin}

latex_engine = "xelatex"

latex_documents = [
    ('index', '{tex_filename}', '{title}', '{author}', 'manual')
]

latex_elements = {{
    "fontpkg": r\"\"\"{styles['fontpkg']}\"\"\",
    "preamble": r\"\"\"{preamble_full}\"\"\",
    "maketitle": r\"\"\"{styles['cover']}\"\"\",
}}

{end}
"""

    conf_path.write_text(conf_text.rstrip() + "\n\n" + block, encoding="utf-8")
    print(f"✔ 已注入 LaTeX 样式：{conf_path}")
