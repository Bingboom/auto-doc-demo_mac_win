#!/usr/bin/env python3
# =============================================================
# Neoway auto-doc | Universal Builder (products × langs × doc_types)
# =============================================================
from pathlib import Path
import subprocess
import sys
import shutil

THIS_FILE = Path(__file__).resolve()
PROJECT_ROOT = THIS_FILE.parents[2]
TOOLS_ROOT   = THIS_FILE.parents[1]

sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(TOOLS_ROOT))

# -------------------------------------------------------------
# Load paths & config
# -------------------------------------------------------------
from tools.utils import path_utils as paths

ROOT = paths.ROOT
CONF = paths.config

LANGUAGES = ["zh_cn", "en"]
PRODUCTS  = list(CONF["products"].keys())
DOC_TYPES = CONF.get("doc_types", {})


def run(cmd, cwd=None):
    print(f"[RUN] {' '.join(cmd)}")
    subprocess.run(cmd, cwd=cwd, check=True)


def build_single(product: str, lang: str, doc_type: str):
    """
    单一组合：产品 × 语言 × 文档类型
    conf.py 会通过 gen_conf 生成
    """

    # -------------------------------
    # ①检查 source 目录是否存在
    # -------------------------------
    src = paths.rst_source_path(product, lang)

    if not src.exists():
        print(f"[SKIP] {product} [{lang}] <{doc_type}> - source dir not found: {src}")
        return

    # 生成 conf.py —— 基于模板
    from tools.gen_conf import generate_conf
    generate_conf(product, lang, doc_type)

    # 计算路径
    html_out = paths.build_html_path(product, lang)
    pdf_out  = paths.build_pdf_path(product, lang)

    html_out.mkdir(parents=True, exist_ok=True)
    pdf_out.mkdir(parents=True, exist_ok=True)

    print(f"\n==== Building {product} [{lang}] <{doc_type}> ====")

    # ---------------------------
    # HTML
    # ---------------------------
    run(["sphinx-build", "-b", "html", str(src), str(html_out)])

    # ---------------------------
    # LaTeX
    # ---------------------------
    run(["sphinx-build", "-b", "latex", str(src), str(pdf_out)])

    # ---------------------------
    # 寻找 .tex 文件（不再依赖 Manual 关键字）
    # ---------------------------
    tex_candidates = [
        t for t in pdf_out.glob("*.tex")
        if not t.name.startswith("sphinx")
    ]

    if not tex_candidates:
        print("[WARN] 未找到可用的 .tex 文件（跳过 PDF）")
        return

    tex_file = tex_candidates[0]   # 取第一个有效 tex 文件

    # ---------------------------
    # PDF 编译
    # ---------------------------
    run([
        "latexmk", "-xelatex", "-interaction=nonstopmode", "-f", tex_file.name
    ], cwd=str(pdf_out))

    # ⭐ 修改 PDF 匹配规则
    pdf_candidates = [
        f for f in pdf_out.glob("*.pdf")
        if not f.name.startswith("sphinx")
    ]

    if not pdf_candidates:
        print("[WARN] PDF 未生成")
        return

    final_pdf = pdf_candidates[0]


    # 自动命名 PDF
    pdf_name = DOC_TYPES[doc_type][lang]   # AT命令手册 / AT Commands Manual
    publish_dir = ROOT / "output" / "pdf"
    publish_dir.mkdir(parents=True, exist_ok=True)

    renamed = publish_dir / f"{product}_{pdf_name}_{lang}.pdf"
    shutil.copy2(final_pdf, renamed)

    print(f"[OK] {product} [{lang}] <{doc_type}> → {renamed}")


def build_all():
    for product in PRODUCTS:
        product_cfg = CONF["products"][product]
        doc_types = product_cfg.get("doc_types", ["AT"])

        for doc_type in doc_types:
            for lang in LANGUAGES:
                build_single(product, lang, doc_type)


if __name__ == "__main__":
    build_all()
