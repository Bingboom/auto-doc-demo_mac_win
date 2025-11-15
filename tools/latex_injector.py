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
    # 只改 cleardoublepage，不动 clearpage 和目录逻辑
    remove_openright_blank_patch = r"""
% ===== Neoway patch: remove blank pages from openright/cleardoublepage =====
\makeatletter
\let\origcleardoublepage\cleardoublepage
\renewcommand{\cleardoublepage}{\clearpage}
\makeatother
"""

    patched_preamble = styles["preamble_full"].rstrip() + "\n" + remove_openright_blank_patch

    # 注入 block
    block = f"""
{marker_begin}

latex_engine = "xelatex"

# 生成 LaTeX 主文件名（必须设置，否则默认 projectnamenotset）
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
    print(f"✔ 已注入 LaTeX 样式和 latex_documents（含 cleardoublepage 补丁）：{conf_path}")
