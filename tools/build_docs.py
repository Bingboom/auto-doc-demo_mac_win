#!/usr/bin/env python3
# =============================================================
# Neoway auto-doc | Safe Universal Builder (models × languages)
# =============================================================
from pathlib import Path
import subprocess
import sys
import shutil

# -------------------------------------------------------------
# 1. 强制定位仓库根目录（防止 Sphinx cwd 干扰）
# -------------------------------------------------------------
THIS_FILE = Path(__file__).resolve()
PROJECT_ROOT = THIS_FILE.parents[2]     # auto-doc-demo_mac_win/
TOOLS_ROOT   = THIS_FILE.parents[1]     # tools/

# 避免 import tools 失败
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(TOOLS_ROOT))

import tools.utils.path_utils as paths

ROOT = paths.ROOT
CONF = paths.config

LANGUAGES = ["zh_CN", "en"]
PRODUCTS  = list(CONF["products"].keys())


def run(cmd, cwd=None):
    print(f"[RUN] {' '.join(cmd)}")
    subprocess.run(cmd, cwd=cwd, check=True)


def build_single(product: str, lang: str):
    """构建单一产品 + 单一语言。不存在语言目录则自动跳过。"""

    conf_py = ROOT / f"docs/{product}/{lang}/source/conf.py"

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
    # 1. HTML
    # ---------------------------
    run([
        "sphinx-build",
        "-b", "html",
        str(source_dir),
        str(html_out)
    ])

    # ---------------------------
    # 2. LaTeX（生成 tex 文件）
    # ---------------------------
    run([
        "sphinx-build",
        "-b", "latex",
        str(source_dir),
        str(pdf_out)
    ])

    # ---------------------------
    # 3. PDF（只编译主 Manual.tex）
    # ---------------------------
    tex_file = None
    for t in pdf_out.glob("*.tex"):
        if "Manual" in t.name:
            tex_file = t
            break

    if not tex_file:
        print(f"[WARN] {product} [{lang}] 未找到 *_Manual.tex，跳过 PDF 构建")
        return

    print(f"[PDF] latexmk -xelatex {tex_file.name}")

    run([
        "latexmk",
        "-xelatex",
        tex_file.name
    ], cwd=str(pdf_out))

    # ---------------------------
    # 4. PDF 发布流程（重命名 + 复制到 output/pdf）
    # ---------------------------
    final_pdf = None
    for f in pdf_out.glob("*.pdf"):
        if "Manual" in f.name:
            final_pdf = f
            break

    if not final_pdf:
        print(f"[WARN] {product} [{lang}] 未找到 PDF，跳过发布")
        return

    # 创建输出目录
    publish_dir = ROOT / "output" / "pdf"
    publish_dir.mkdir(parents=True, exist_ok=True)

    # 目标文件名：Neoway_<Model>_<Lang>.pdf
    renamed = publish_dir / f"Neoway_{product}_{lang}.pdf"

    print(f"[PUBLISH] {final_pdf.name} → {renamed}")

    shutil.copy2(final_pdf, renamed)

    print(f"[OK] 完成 {product} [{lang}] 构建（HTML + PDF + 发布）")


def build_all():
    for product in PRODUCTS:
        for lang in LANGUAGES:
            build_single(product, lang)


if __name__ == "__main__":
    build_all()
