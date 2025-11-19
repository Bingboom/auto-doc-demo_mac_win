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


# -------------------------------------------------------------
# 执行命令
# -------------------------------------------------------------
def run(cmd, cwd=None):
    print(f"[RUN] {' '.join(cmd)}")
    subprocess.run(cmd, cwd=cwd, check=True)


# -------------------------------------------------------------
# 识别 main.tex（排除 headerfooter / sphinxmessages 等）
# -------------------------------------------------------------
def is_main_tex(f: Path) -> bool:
    BAD_NAMES = {
        "headerfooter.tex",
        "sphinxmessages.tex",
        "python.tex",
        "footer.tex",
    }

    if f.name in BAD_NAMES:
        return False
    if f.name.startswith("sphinx"):
        return False
    if f.name.startswith("latexmk"):
        return False

    # 内容必须包含 \begin{document}
    try:
        text = f.read_text(encoding="utf-8", errors="ignore")
        if r"\begin{document}" not in text:
            return False
    except:
        return False

    return True


# -------------------------------------------------------------
# 构建单一组合：产品 × 语言 × 文档类型
# -------------------------------------------------------------
def build_single(product: str, lang: str, doc_type: str):

    # -------------------------------
    # ①检查 source 是否存在
    # -------------------------------
    src = paths.rst_source_path(product, lang)

    if not src.exists():
        print(f"[SKIP] {product} [{lang}] <{doc_type}> - source dir not found: {src}")
        return

    # -------------------------------
    # ②生成 conf.py
    # -------------------------------
    from tools.gen_conf import generate_conf
    generate_conf(product, lang, doc_type)

    # 输出路径
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
    # ③ 查找正确 main.tex
    # ---------------------------
    tex_files = list(pdf_out.glob("*.tex"))
    main_tex_list = [f for f in tex_files if is_main_tex(f)]

    if not main_tex_list:
        print("[WARN] 未找到 main.tex，跳过 PDF")
        return

    tex_file = main_tex_list[0]
    print(f"[TEX] Using main tex: {tex_file.name}")

    # ---------------------------
    # ④ PDF 编译
    # ---------------------------
    run([
        "latexmk", "-xelatex", "-interaction=nonstopmode", "-f", tex_file.name
    ], cwd=str(pdf_out))

    # ---------------------------
    # ⑤ 查找生成的 PDF（排除 sphinxmessages）
    # ---------------------------
    pdf_candidates = [
        f for f in pdf_out.glob("*.pdf")
        if not f.name.startswith("sphinx")
    ]

    if not pdf_candidates:
        print("[WARN] PDF 未生成")
        return

    final_pdf = pdf_candidates[0]

    # ---------------------------
    # ⑥ 自动命名 PDF（来自 config.yaml）
    # ---------------------------
    pdf_name = DOC_TYPES[doc_type][lang]   # e.g., AT命令手册 / AT Commands Manual

    publish_dir = ROOT / "output" / "pdf"
    publish_dir.mkdir(parents=True, exist_ok=True)

    renamed = publish_dir / f"{product}_{pdf_name}_{lang}.pdf"
    shutil.copy2(final_pdf, renamed)

    print(f"[OK] {product} [{lang}] <{doc_type}> → {renamed}")


# -------------------------------------------------------------
# 构建全量
# -------------------------------------------------------------
def build_all():
    for product in PRODUCTS:
        product_cfg = CONF["products"][product]
        doc_types = product_cfg.get("doc_types", ["AT"])

        for doc_type in doc_types:
            for lang in LANGUAGES:
                build_single(product, lang, doc_type)


if __name__ == "__main__":
    build_all()
