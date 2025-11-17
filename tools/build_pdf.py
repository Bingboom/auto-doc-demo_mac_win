#!/usr/bin/env python3
# tools/build_pdf.py

import sys
import shutil
import subprocess
import importlib
from pathlib import Path

# ============================================================
# 🔧 统一路径体系
# ============================================================
from utils.path_utils import (
    get_default_product,
    rst_source_path,
    build_pdf_path,
    latex_common_path,
    static_images_path,
)

# 默认产品线
PRODUCT = get_default_product()

# 路径体系
RST_SOURCE = rst_source_path(PRODUCT)
PDF_ROOT = build_pdf_path(PRODUCT)
LATEX_COMMON = latex_common_path()
STATIC_IMAGES = static_images_path()

LATEX_BUILD = PDF_ROOT / "latex"
LATEX_BUILD.mkdir(parents=True, exist_ok=True)

# ============================================================
# 🔧 工具函数
# ============================================================
def run_cmd(cmd, cwd=None):
    print(f"\n$ {' '.join(cmd)}")
    p = subprocess.run(cmd, cwd=cwd)
    if p.returncode != 0:
        raise RuntimeError(f"命令失败：{' '.join(cmd)}")

def clean_latex_dir(pdf_dir: Path):
    exts = [
        ".aux", ".log", ".toc", ".out", ".idx",
        ".ind", ".ilg", ".lof", ".lot",
        ".fls", ".fdb_latexmk",
        ".tex"
    ]
    for f in pdf_dir.iterdir():
        if f.suffix.lower() in exts:
            f.unlink()

def copy_static_assets():
    allowed = [".png", ".jpg", ".jpeg", ".pdf", ".sty", ".cls"]
    target = LATEX_BUILD
    target.mkdir(parents=True, exist_ok=True)

    for folder in [LATEX_COMMON, STATIC_IMAGES]:
        for f in folder.iterdir():
            if f.is_file() and f.suffix.lower() in allowed:
                shutil.copy(f, target)

# ============================================================
# 🔧 主构建流程
# ============================================================
def build_pdf(model, version, doc_type, author):

    print("\n============================")
    print("🚀 开始构建 PDF")
    print("============================\n")

    # 导入 latex 模块
    from latex_cover import render_cover
    from latex_styles import load_latex_styles
    from latex_injector import inject_latex_block

    # 生成封面
    render_cover(model, version, doc_type)

    styles = load_latex_styles()

    conf_path = RST_SOURCE / "conf.py"
    inject_latex_block(conf_path, model, version, doc_type, author, styles)
    print("✔ 已注入 LaTeX 样式")

    clean_latex_dir(LATEX_BUILD)
    copy_static_assets()
    print("✔ 已复制静态资源")

    # Sphinx → LaTeX
    run_cmd(
        ["sphinx-build", "-b", "latex", str(RST_SOURCE), str(LATEX_BUILD)]
    )

    main_tex_name = f"Neoway_{model}_Manual.tex"
    tex_file = LATEX_BUILD / main_tex_name

    if not tex_file.exists():
        available = [p.name for p in LATEX_BUILD.glob("*.tex")]
        raise FileNotFoundError(
            f"❌ 未找到主 TeX 文件：{main_tex_name}\n可用：{available}"
        )

    print(f"✔ 找到主 tex：{main_tex_name}")
    print("== xelatex 编译中 ==")

    for i in range(3):
        run_cmd(["xelatex", "-interaction=nonstopmode", tex_file.name], cwd=LATEX_BUILD)

    idx = tex_file.with_suffix(".idx")
    if idx.exists():
        run_cmd(["makeindex", idx.name], cwd=LATEX_BUILD)

    for i in range(2):
        run_cmd(["xelatex", "-interaction=nonstopmode", tex_file.name], cwd=LATEX_BUILD)

    final_pdf = tex_file.with_suffix(".pdf")
    output_pdf = PDF_ROOT / f"Neoway_{model}_{doc_type.replace(' ','_')}.pdf"
    shutil.copy(final_pdf, output_pdf)

    print(f"\n🎉 PDF 构建成功：{output_pdf}\n")


if __name__ == "__main__":
    build_pdf(
        model=PRODUCT,
        version="v1.0",
        doc_type="AT_Command_Manual",
        author="Neoway Documentation Team",
    )
