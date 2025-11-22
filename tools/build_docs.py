#!/usr/bin/env python3
# =============================================================
# Neoway auto-doc | Universal Builder (paths unified + stable)
# =============================================================
from pathlib import Path
import subprocess
import shutil
import platform
import sys

# -------------------------------------------------------------
# ① 统一路径初始化（确保能 import tools.*）
# -------------------------------------------------------------
THIS_FILE = Path(__file__).resolve()
TOOLS_DIR = THIS_FILE.parent            # tools/
PROJECT_ROOT = TOOLS_DIR.parent         # 仓库根目录

# 注入 Python 搜索路径（必须保留）
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(TOOLS_DIR))

# -------------------------------------------------------------
# ② 导入 path_utils（中央路径系统）
# -------------------------------------------------------------
from tools.utils import path_utils as paths

ROOT = paths.ROOT
CONF = paths.config

LANGUAGES = ["zh_cn", "en"]
PRODUCTS  = list(CONF["products"].keys())
DOC_TYPES = CONF.get("doc_types", {})

# =============================================================
# ③ 自动生成 fonts.tex
# =============================================================
def generate_fonts_tex():

    cfg = CONF
    os_name = platform.system().lower()

    if "windows" in os_name:
        key = "windows"
    elif "darwin" in os_name:
        key = "mac"
    else:
        key = "linux"

    font_cfg = cfg["fonts"][key]

    cjk  = font_cfg["cjk"]
    sans = font_cfg["sans"]
    mono = font_cfg["mono"]

    fonts_tex = f"""
% ======= AUTO GENERATED: Do NOT edit manually =======
% Platform: {key}

\\usepackage{{xeCJK}}
\\usepackage{{fontspec}}

% ---- Western ----
\\setmainfont{{Times New Roman}}
\\setsansfont{{{sans}}}
\\setmonofont{{{mono}}}

% ---- CJK ----
\\setCJKmainfont{{{cjk}}}
\\setCJKsansfont{{{cjk}}}
\\setCJKmonofont{{{cjk}}}

% ---- Fallback ----
\\defaultCJKfontfeatures{{
    Script=Hans,
    Language=Chinese
}}
"""

    out_path = paths.latex_common_path() / "fonts.tex"
    out_path.write_text(fonts_tex, encoding="utf-8")
    print(f"[FONTS] Generated fonts.tex → {out_path}")

# =============================================================
# ④ run() — 执行命令
# =============================================================
def run(cmd, cwd=None):
    print(f"[RUN] {' '.join(cmd)}")
    subprocess.run(cmd, cwd=cwd, check=True)

# =============================================================
# ⑤ 识别 main.tex（跳过非主入口）
# =============================================================
def is_main_tex(f: Path) -> bool:
    BAD = {"headerfooter.tex", "sphinxmessages.tex", "python.tex", "footer.tex"}

    if f.name in BAD:
        return False
    if f.name.startswith("sphinx") or f.name.startswith("latexmk"):
        return False

    try:
        text = f.read_text(encoding="utf-8", errors="ignore")
        return r"\begin{document}" in text
    except:
        return False


# =============================================================
# ⑥ 构建单个 product × lang × doc_type
# =============================================================
def build_single(product: str, lang: str, doc_type: str):

    src = paths.rst_source_path(product, lang)

    if not src.exists():
        print(f"[SKIP] source 不存在: {src}")
        return

    # --- 生成 conf.py ---
    from tools.gen_conf import generate_conf
    generate_conf(product, lang, doc_type)

    html_out = paths.build_html_path(product, lang)
    pdf_out  = paths.build_pdf_path(product, lang)

    html_out.mkdir(parents=True, exist_ok=True)
    pdf_out.mkdir(parents=True, exist_ok=True)

    print(f"\n==== Building {product} [{lang}] <{doc_type}> ====")

    # --- HTML ---
    run(["sphinx-build", "-b", "html", str(src), str(html_out)])

    # --- LaTeX ---
    run(["sphinx-build", "-b", "latex", str(src), str(pdf_out)])

    # --- 找 main.tex ---
    tex_files = list(pdf_out.glob("*.tex"))
    main_list = [f for f in tex_files if is_main_tex(f)]

    if not main_list:
        print("[WARN] main.tex 未找到，跳过 PDF")
        return

    tex_file = main_list[0]
    print(f"[TEX] Using: {tex_file.name}")

    # --- latex clean ---
    run(["latexmk", "-C"], cwd=pdf_out)

    # --- 编译 PDF ---
    run(["latexmk", "-xelatex", "-interaction=nonstopmode", "-f", tex_file.name],
        cwd=pdf_out)

    # --- 找最终 PDF ---
    pdf_candidates = [f for f in pdf_out.glob("*.pdf")
                      if not f.name.startswith("sphinx")]

    if not pdf_candidates:
        print("[WARN] PDF 未生成")
        return

    final_pdf = pdf_candidates[0]

    # --- 自动重命名 ---
    pdf_name = DOC_TYPES[doc_type][lang]

    publish_dir = ROOT / "output" / "pdf"
    publish_dir.mkdir(parents=True, exist_ok=True)

    renamed = publish_dir / f"{product}_{pdf_name}_{lang}.pdf"
    shutil.copy2(final_pdf, renamed)

    print(f"[OK] PDF → {renamed}")

# =============================================================
# ⑦ 构建全量
# =============================================================
def build_all():

    generate_fonts_tex()

    for product in PRODUCTS:
        doc_types = CONF["products"][product].get("doc_types", ["AT"])
        for doc_type in doc_types:
            for lang in LANGUAGES:
                build_single(product, lang, doc_type)

if __name__ == "__main__":
    build_all()
