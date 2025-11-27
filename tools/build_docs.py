#!/usr/bin/env python3
# =============================================================
# Auto-Doc Next-Gen | Ultra-Stable PDF Builder (3-Pass XeLaTeX)
# =============================================================
# ✔ 不使用 latexmk（避免 TL2025 错误）
# ✔ 三次 XeLaTeX 稳定排版（封面·目录·引用）
# ✔ 清理 latex 临时文件（第一次构建最关键）
# ✔ theme.tex 不含字体，字体全部在 fonts.tex
# =============================================================

from pathlib import Path
import subprocess
import shutil
import sys
from jinja2 import Template

# ---------------- Path Bootstrapping ----------------
THIS = Path(__file__).resolve()
TOOLS = THIS.parent
ROOT = TOOLS.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(TOOLS))

from tools.utils import path_utils as paths
from tools.utils.theme_loader import load_pdf_theme

CONF = paths.config
LANGUAGES = CONF["languages"]
PRODUCTS = list(CONF["products"].keys())
DOC_TYPES = CONF.get("doc_types", {})

# =============================================================
# run_live：实时输出（不吞日志）
# =============================================================
def run_live(cmd, cwd=None):
    print(f"\n[CMD] {' '.join(cmd)}\n")
    proc = subprocess.Popen(
        cmd,
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
    )
    for line in proc.stdout:
        print(line, end="")
    proc.wait()
    return proc.returncode


# =============================================================
# 清理 LaTeX 临时文件 + 删除 latexmkrc
# =============================================================
TEMP_EXT = [
    "*.aux", "*.log", "*.toc", "*.out", "*.idx", "*.ind", "*.ilg",
    "*.lof", "*.lot", "*.fls", "*.fdb_latexmk", "*.nav", "*.snm",
    "*.bbl", "*.blg", "*.synctex.gz"
]

def clean_latex_temp(pdf_dir: Path):
    for pattern in TEMP_EXT:
        for f in pdf_dir.glob(pattern):
            try:
                f.unlink()
            except:
                pass

    for f in pdf_dir.glob("latexmkrc"):
        f.unlink()
        print("[FIX] removed latexmkrc")


# =============================================================
# 渲染 theme.tex（不注入 fonts）
# =============================================================
def render_theme(theme_name, product, lang, pdf_dir):
    theme_cfg, theme_files = load_pdf_theme(theme_name)
    tpl_file = theme_files["theme"]

    # logo 路径
    logo = CONF["common"]["header_logo"].get(product, CONF["common"]["header_logo"]["default"])
    header_logo = (paths.static_images_path() / logo).as_posix()

    # cover 背景
    bg = CONF["common"]["cover_background"].get(product, CONF["common"]["cover_background"]["default"])
    cover_bg = (paths.static_images_path() / bg).as_posix()

    # ⚠ 不再把 fonts 注入 theme.tex
    ctx = {
        "header_logo": header_logo,
        "theme": theme_cfg,
        "cover_background": cover_bg,
    }

    tpl = Template(tpl_file.read_text(encoding="utf-8"))
    out = pdf_dir / "theme.tex"
    out.write_text(tpl.render(**ctx), encoding="utf-8")
    print(f"[THEME] written → {out}")


# =============================================================
# 查找 main.tex
# =============================================================
def find_main_tex(pdf_dir: Path):
    for f in pdf_dir.glob("*.tex"):
        if "\\begin{document}" in f.read_text(encoding="utf-8", errors="ignore"):
            return f
    return None


# =============================================================
# 三次 xelatex
# =============================================================
def run_xelatex_3pass(tex_main: str, cwd: Path):
    for i in range(3):
        print(f"\n[XELATEX] pass {i+1}/3 ...")
        code = run_live(["xelatex", "-interaction=nonstopmode", "-halt-on-error", tex_main], cwd=cwd)
        if code != 0:
            print(f"[ERROR] xelatex failed at pass {i+1}")
            return False
    return True


# =============================================================
# 构建单文档
# =============================================================
def build_single(product, lang, doc_type):
    src = paths.rst_source_path(product, lang)
    if not src.exists():
        print(f"[SKIP] no source: {src}")
        return

    from tools.gen_conf import generate_conf
    generate_conf(product, lang, doc_type)

    html_out = paths.build_html_path(product, lang)
    pdf_out  = paths.build_pdf_path(product, lang)
    html_out.mkdir(parents=True, exist_ok=True)
    pdf_out.mkdir(parents=True, exist_ok=True)

    print(f"\n==== Building {product} [{lang}] <{doc_type}> ====")

    run_live(["sphinx-build", "-b", "html", str(src), str(html_out)])
    run_live(["sphinx-build", "-b", "latex", str(src), str(pdf_out)])

    clean_latex_temp(pdf_out)

    theme = CONF["products"][product].get("pdf_theme", CONF["theme"]["pdf_default"])
    render_theme(theme, product, lang, pdf_out)

    tex_main = find_main_tex(pdf_out)
    if not tex_main:
        print("[ERROR] main.tex not found")
        return
    print(f"[TEX] using → {tex_main.name}")

    ok = run_xelatex_3pass(tex_main.name, pdf_out)
    if not ok:
        print("[ERROR] PDF compile failed")
        return

    pdf_files = list(pdf_out.glob("*.pdf"))
    if not pdf_files:
        print("[ERROR] no PDF produced")
        return

    final_pdf = pdf_files[0]
    pdf_name = DOC_TYPES[doc_type][lang]
    out_dir = paths.output_pdf_dir()
    out_dir.mkdir(parents=True, exist_ok=True)

    out = out_dir / f"{product}_{pdf_name}_{lang}.pdf"
    shutil.copy2(final_pdf, out)
    print(f"[OK] PDF exported → {out}")


# =============================================================
# 全量构建
# =============================================================
def build_all():
    for product in PRODUCTS:
        for doc_type in CONF["products"][product].get("doc_types", ["AT"]):
            for lang in LANGUAGES:
                build_single(product, lang, doc_type)


if __name__ == "__main__":
    build_all()
