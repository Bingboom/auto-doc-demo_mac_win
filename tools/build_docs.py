#!/usr/bin/env python3
# =============================================================
# Auto-Doc Next-Gen | Ultra-Stable PDF Builder (3-Pass XeLaTeX)
# =============================================================
# 📌 核心目标
#   - 不使用 latexmk（彻底避免 TL2025 的 hang / exit=12）
#   - 使用 xelatex 三次构建（第一次排版，第二次目录，第三次引用稳定）
#   - theme.tex 完全不含字体（由 fonts.tex 接管字体体系）
#   - 可长期维护、结构清晰、通用化无定制
#   - 任何产品 / 语言 都可复用，不依赖业务特性
# =============================================================

from pathlib import Path
import subprocess
import shutil
import sys
from jinja2 import Template

# =============================================================
# ① Path Bootstrapping
#    —— 注入 ROOT, TOOLS，确保 tools.* 可 import
# =============================================================
THIS = Path(__file__).resolve()
TOOLS = THIS.parent
ROOT = TOOLS.parent

sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(TOOLS))

# 模块化路径系统
from tools.utils import path_utils as paths
from tools.utils.theme_loader import load_pdf_theme

# 加载全局配置
CONF = paths.config
LANGUAGES = CONF["languages"]
PRODUCTS = list(CONF["products"].keys())
DOC_TYPES = CONF.get("doc_types", {})

# =============================================================
# ② run_live：实时输出命令行，避免卡住
# =============================================================
def run_live(cmd, cwd=None):
    """
    实时输出 stdout + stderr（不吞日志）
    解决 subprocess.run 卡住的问题。
    """
    print(f"\n[CMD] {' '.join(cmd)}\n")
    proc = subprocess.Popen(
        cmd,
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    for line in proc.stdout:
        print(line, end="")
    proc.wait()
    return proc.returncode


# =============================================================
# ③ 清理临时文件（第一次构建必备）
# =============================================================
TEMP_EXT = [
    "*.aux", "*.log", "*.toc", "*.out", "*.idx", "*.ind", "*.ilg",
    "*.lof", "*.lot", "*.fls", "*.fdb_latexmk", "*.nav", "*.snm",
    "*.bbl", "*.blg", "*.synctex.gz"
]

def clean_latex_temp(pdf_dir: Path):
    """
    删除所有 LaTeX 临时文件
    删除 Sphinx 生成的 latexmkrc（彻底禁用 latexmk）
    """
    for pattern in TEMP_EXT:
        for f in pdf_dir.glob(pattern):
            try:
                f.unlink()
            except:
                pass

    # 禁用 latexmkrc —— TL2025 会出兼容问题
    for f in pdf_dir.glob("latexmkrc"):
        f.unlink()
        print("[FIX] removed latexmkrc")


# =============================================================
# ④ 渲染 theme.tex（注意：不注入字体）
# =============================================================
def render_theme(theme_name, product, lang, pdf_dir):
    """
    渲染 theme.tex（包含颜色、页眉、封面背景等）
    字体不应在这里配置（fonts.tex 会全局加载）
    """
    theme_cfg, theme_files = load_pdf_theme(theme_name)
    tpl_file = theme_files["theme"]

    # logo
    logo = CONF["common"]["header_logo"].get(
        product, CONF["common"]["header_logo"]["default"]
    )
    header_logo = (paths.static_images_path() / logo).as_posix()

    # cover 背景图
    bg = CONF["common"]["cover_background"].get(
        product, CONF["common"]["cover_background"]["default"]
    )
    cover_bg = (paths.static_images_path() / bg).as_posix()

    # ⚠ 字体不注入这里
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
# ⑤ 查找 main.tex（含 \begin{document} 的那个）
# =============================================================
def find_main_tex(pdf_dir: Path):
    for f in pdf_dir.glob("*.tex"):
        if "\\begin{document}" in f.read_text(encoding="utf-8", errors="ignore"):
            return f
    return None


# =============================================================
# ⑥ 稳定的三次 XeLaTeX 构建流程
# =============================================================
def run_xelatex_3pass(tex_main: str, cwd: Path):
    """
    Pass 1：基础排版
    Pass 2：修复 TOC 页码
    Pass 3：让引用/页码完全稳定
    """
    for i in range(3):
        print(f"\n[XELATEX] pass {i+1}/3 ...")
        code = run_live(
            ["xelatex", "-interaction=nonstopmode", "-halt-on-error", tex_main],
            cwd=cwd
        )
        if code != 0:
            print(f"[ERROR] xelatex failed at pass {i+1}")
            return False
    return True


# =============================================================
# ⑦ 构建单个 PDF 文档
# =============================================================
def build_single(product, lang, doc_type):
    # ---------- 解析路径 ----------
    src = paths.rst_source_path(product, lang)
    if not src.exists():
        print(f"[SKIP] source missing: {src}")
        return

    # ---------- 写 conf.py ----------
    from tools.gen_conf import generate_conf
    generate_conf(product, lang, doc_type)

    html_out = paths.build_html_path(product, lang)
    pdf_out = paths.build_pdf_path(product, lang)
    html_out.mkdir(parents=True, exist_ok=True)
    pdf_out.mkdir(parents=True, exist_ok=True)

    print(f"\n==== Building {product} [{lang}] <{doc_type}> ====")

    # ---------- Sphinx 构建 ----------
    run_live(["sphinx-build", "-b", "html", str(src), str(html_out)])
    run_live(["sphinx-build", "-b", "latex", str(src), str(pdf_out)])

    # ---------- 清理 Sphinx 遗留 ----------
    clean_latex_temp(pdf_out)

    # ---------- 渲染 theme.tex ----------
    theme = CONF["products"][product].get("pdf_theme", CONF["theme"]["pdf_default"])
    render_theme(theme, product, lang, pdf_out)

    # ---------- 找 main.tex ----------
    tex_main = find_main_tex(pdf_out)
    if not tex_main:
        print("[ERROR] main.tex not found")
        return
    print(f"[TEX] using → {tex_main.name}")

    # ---------- 三次 xelatex ----------
    ok = run_xelatex_3pass(tex_main.name, pdf_out)
    if not ok:
        print("[ERROR] PDF compile failed")
        return

    # ---------- 找生成的 PDF ----------
    pdf_files = list(pdf_out.glob("*.pdf"))
    if not pdf_files:
        print("[ERROR] no PDF produced")
        return

    final_pdf = pdf_files[0]

    # ---------- 输出到统一 output/pdf ----------
    pdf_name = DOC_TYPES[doc_type][lang]
    out_dir = paths.output_pdf_dir()
    out_dir.mkdir(parents=True, exist_ok=True)

    out = out_dir / f"{product}_{pdf_name}_{lang}.pdf"
    shutil.copy2(final_pdf, out)
    print(f"[OK] PDF exported → {out}")


# =============================================================
# ⑧ 全量构建
# =============================================================
def build_all():
    for product in PRODUCTS:
        for doc_type in CONF["products"][product].get("doc_types", ["AT"]):
            for lang in LANGUAGES:
                build_single(product, lang, doc_type)


# =============================================================
# 入口
# =============================================================
if __name__ == "__main__":
    build_all()
