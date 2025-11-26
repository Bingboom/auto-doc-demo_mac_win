#!/usr/bin/env python3
# =============================================================
# Neoway auto-doc | Universal Builder (NO hard-coded paths)
# =============================================================
from pathlib import Path
import subprocess
import shutil
import platform
import sys

# -------------------------------------------------------------
# ① 初始化路径（必须放前面）
# -------------------------------------------------------------
THIS_FILE = Path(__file__).resolve()
TOOLS_DIR = THIS_FILE.parent
PROJECT_ROOT = TOOLS_DIR.parent

sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(TOOLS_DIR))

# -------------------------------------------------------------
# ② path_utils（中央路径管理）
# -------------------------------------------------------------
from tools.utils import path_utils as paths

ROOT = paths.ROOT
CONF = paths.config

LANGUAGES = CONF["languages"]                 # ← 从 config.yaml 读
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

    fonts_tex = f"""
% ======= AUTO GENERATED =======
% Platform: {key}

\\usepackage{{xeCJK}}
\\usepackage{{fontspec}}

\\setmainfont{{Times New Roman}}
\\setsansfont{{{font_cfg['sans']}}}
\\setmonofont{{{font_cfg['mono']}}}

\\setCJKmainfont{{{font_cfg['cjk']}}}
\\setCJKsansfont{{{font_cfg['cjk']}}}
\\setCJKmonofont{{{font_cfg['cjk']}}}

\\defaultCJKfontfeatures{{ Script=Hans, Language=Chinese }}
"""

    out_path = paths.latex_common_path() / "fonts.tex"
    out_path.write_text(fonts_tex, encoding="utf-8")
    print(f"[FONTS] Generated → {out_path}")


# =============================================================
# ④ run()
# =============================================================
def run(cmd, cwd=None):
    print(f"[RUN] {' '.join(cmd)}")
    try:
        subprocess.run(cmd, cwd=cwd, check=True)
    except subprocess.CalledProcessError as e:
        # Exit code 12 = rerun needed (common in index builds), but not fatal.
        if e.returncode == 12:
            print("[INFO] latexmk exit code 12 ignored (PDF already generated or rerun needed)")
        else:
            raise



# =============================================================
# ⑤ 判断 main.tex
# =============================================================
def is_main_tex(f: Path) -> bool:
    if f.name.startswith(("sphinx", "latexmk")):
        return False
    if f.name in {"headerfooter.tex", "python.tex", "footer.tex"}:
        return False
    try:
        text = f.read_text(encoding="utf-8", errors="ignore")
        return r"\begin{document}" in text
    except:
        return False


# =============================================================
# ⑥ 构建单个组合
# =============================================================
def build_single(product: str, lang: str, doc_type: str):

    src = paths.rst_source_path(product, lang)
    if not src.exists():
        print(f"[SKIP] Source 不存在: {src}")
        return

    # 生成 conf.py
    from tools.gen_conf import generate_conf
    generate_conf(product, lang, doc_type)

    html_out = paths.build_html_path(product, lang)
    pdf_out  = paths.build_pdf_path(product, lang)

    html_out.mkdir(parents=True, exist_ok=True)
    pdf_out.mkdir(parents=True, exist_ok=True)

    print(f"\n==== Building {product} [{lang}] <{doc_type}> ====")

    run(["sphinx-build", "-b", "html", str(src), str(html_out)])
    run(["sphinx-build", "-b", "latex", str(src), str(pdf_out)])
    # ===== Copy latex common templates (fonts.tex / header / footer / esp_at_style.tex etc.) =====
    latex_common = paths.latex_common_path()     # docs/_common/latex_templates
    for tex in latex_common.glob("*.tex"):
        shutil.copy2(tex, pdf_out)    

    tex_files = list(pdf_out.glob("*.tex"))
    main_list = [f for f in tex_files if is_main_tex(f)]
    if not main_list:
        print("[WARN] main.tex 未找到")
        return

    tex_file = main_list[0]
    print(f"[TEX] Using: {tex_file.name}")

    run(["latexmk", "-C"], cwd=pdf_out)
    run(["latexmk", "-xelatex", "-interaction=nonstopmode", "-f", tex_file.name],
        cwd=pdf_out)
    
    run(["latexmk", "-xelatex", "-interaction=nonstopmode", "-halt-on-error", tex_file.name],
    cwd=pdf_out)


    pdf_candidates = [f for f in pdf_out.glob("*.pdf")
                      if not f.name.startswith("sphinx")]

    if not pdf_candidates:
        print("[WARN] PDF 未生成")
        return

    final_pdf = pdf_candidates[0]

    pdf_name = DOC_TYPES[doc_type][lang]

    publish_dir = paths.output_pdf_dir()        # ← 从 config.yaml
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
