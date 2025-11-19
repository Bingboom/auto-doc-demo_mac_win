#!/usr/bin/env python3
# =============================================================
# Neoway auto-doc | Universal Builder (products × languages)
# =============================================================
from pathlib import Path
import subprocess
import sys
import shutil

# -------------------------------------------------------------
# 1. 强制定位仓库根目录
# -------------------------------------------------------------
THIS_FILE = Path(__file__).resolve()
PROJECT_ROOT = THIS_FILE.parents[2]
TOOLS_ROOT   = THIS_FILE.parents[1]

sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(TOOLS_ROOT))

# -------------------------------------------------------------
# 引入 path_utils
# -------------------------------------------------------------
from tools.utils import path_utils as paths

ROOT = paths.ROOT
CONF = paths.config

LANGUAGES = ["zh_CN", "en"]
PRODUCTS  = list(CONF["products"].keys())


def run(cmd, cwd=None):
    print(f"[RUN] {' '.join(cmd)}")
    subprocess.run(cmd, cwd=cwd, check=True)


def build_single(product: str, lang: str):
    """匹配新目录结构：docs/<lang>/<product>/source/conf.py"""

    conf_py = ROOT / f"docs/{lang}/{product}/source/conf.py"

    if not conf_py.exists():
        print(f"[SKIP] {product} [{lang}] - 未找到 {conf_py}")
        return

    print(f"\n==== Building {product} [{lang}] ====")

    source_dir = conf_py.parent
    html_out   = paths.build_html_path(product, lang)
    pdf_out    = paths.build_pdf_path(product, lang)

    html_out.mkdir(parents=True, exist_ok=True)
    pdf_out.mkdir(parents=True, exist_ok=True)

    # ---------------------------
    # HTML
    # ---------------------------
    run(["sphinx-build", "-b", "html", str(source_dir), str(html_out)])

    # ---------------------------
    # LaTeX
    # ---------------------------
    run(["sphinx-build", "-b", "latex", str(source_dir), str(pdf_out)])

    tex_file = next((t for t in pdf_out.glob("*.tex") if "Manual" in t.name), None)
    if not tex_file:
        print(f"[WARN] 未找到 *_Manual.tex，跳过 PDF")
        return

    # ---------------------------
    # 编译 PDF
    # ---------------------------
    run([
        "latexmk",
        "-xelatex",
        "-interaction=nonstopmode",
        "-f",
        tex_file.name
    ], cwd=str(pdf_out))

    final_pdf = next((f for f in pdf_out.glob("*.pdf") if "Manual" in f.name), None)
    if not final_pdf:
        print(f"[WARN] 未生成 PDF")
        return

    publish_dir = ROOT / "output" / "pdf"
    publish_dir.mkdir(parents=True, exist_ok=True)

    renamed = publish_dir / f"Neoway_{product}_{lang}.pdf"
    shutil.copy2(final_pdf, renamed)

    print(f"[OK] {product} [{lang}] PDF → {renamed}")


def build_all():
    for product in PRODUCTS:
        for lang in LANGUAGES:
            build_single(product, lang)


if __name__ == "__main__":
    build_all()
