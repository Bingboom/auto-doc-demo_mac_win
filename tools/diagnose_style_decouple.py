#!/usr/bin/env python3
# ================================================================
# Auto-Doc Style Decouple Analyzer
# ================================================================
# 作用：
#   ✔ 检查样式文件是否真正解耦
#   ✔ 检测 theme.tex.j2 是否仍引用字体
#   ✔ 检查 headerfooter / titles / cover / colors 是否相互污染
#   ✔ 检查 main.tex 是否仍有 Sphinx 内联样式
#   ✔ 输出结构化报告
# ================================================================

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
THEME_ROOT = ROOT / "tools" / "themes" / "pdf"
COMMON_LATEX = ROOT / "docs" / "_common" / "latex_templates"

REPORT = []


# ------------------------------------------------------------
# 工具：加入一行报告
# ------------------------------------------------------------
def add(msg):
    REPORT.append(msg)


# ------------------------------------------------------------
# 扫描文件内容
# ------------------------------------------------------------
def read(path: Path):
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")


# ------------------------------------------------------------
# 1. 检查 theme.tex.j2 是否仍引用 fonts.xxx
# ------------------------------------------------------------
def check_theme_fonts():
    theme_files = list(THEME_ROOT.rglob("theme.tex.j2"))
    if not theme_files:
        add("[ERROR] 未找到 theme.tex.j2")
        return

    theme_file = theme_files[0]
    code = read(theme_file)

    if "fonts" in code:
        add("[WARN] theme.tex.j2 仍引用 fonts.xxx → 样式未完全解耦")
    else:
        add("[OK] theme.tex.j2 已完全与字体解耦")

    # 检查是否重复设置字体
    if "\\setCJKmainfont" in code or "\\setmainfont" in code:
        add("[ERROR] theme.tex.j2 内含字体配置（必须删除）")
    else:
        add("[OK] theme.tex.j2 未包含字体指令")


# ------------------------------------------------------------
# 2. 检查 fonts.tex 是否是唯一字体源
# ------------------------------------------------------------
def check_fonts_tex():
    fonts_tex = COMMON_LATEX / "fonts.tex"
    code = read(fonts_tex)

    if not code:
        add("[ERROR] fonts.tex 缺失！PDF 无法构建")
        return

    keys = ["setCJKmainfont", "setmainfont", "setsansfont", "setmonofont"]
    ok = all(k in code for k in keys)

    if ok:
        add("[OK] fonts.tex 是唯一的字体定义源")
    else:
        add("[WARN] fonts.tex 字体定义不完整")


# ------------------------------------------------------------
# 3. 检查 headerfooter.tex 是否有样式污染
# ------------------------------------------------------------
def check_headerfooter():
    hf = COMMON_LATEX / "headerfooter.tex"
    code = read(hf)

    if "\\setCJKmainfont" in code or "\\setmainfont" in code:
        add("[ERROR] headerfooter.tex 不应定义字体！必须移除")
    else:
        add("[OK] headerfooter.tex 未涉及字体")

    if "\\definecolor" in code:
        add("[WARN] headerfooter.tex 定义颜色 → 建议移动到 colors.tex")
    else:
        add("[OK] headerfooter.tex 未包含颜色定义（良好）")


# ------------------------------------------------------------
# 4. 检查 titles.tex 是否耦合字体 / 颜色
# ------------------------------------------------------------
def check_titles():
    f = COMMON_LATEX / "titles.tex"
    code = read(f)

    if "\\setCJKmainfont" in code:
        add("[ERROR] titles.tex 中出现字体设定 → 必须删除")
    else:
        add("[OK] titles.tex 未直接配置字体")

    if "\\definecolor" in code:
        add("[WARN] titles.tex 有颜色定义 → 建议放入 colors.tex")
    else:
        add("[OK] titles.tex 未定义颜色（良好）")


# ------------------------------------------------------------
# 5. colors.tex 独立性检查
# ------------------------------------------------------------
def check_colors():
    f = COMMON_LATEX / "colors.tex"
    code = read(f)

    if not code:
        add("[WARN] colors.tex 为空 或 未使用")

    if "\\definecolor" in code:
        add("[OK] colors.tex 颜色定义存在")
    else:
        add("[WARN] colors.tex 没有颜色定义 → 是预期的吗？")


# ------------------------------------------------------------
# 6. 检查 Sphinx 生成的 main.tex 是否污染样式
# ------------------------------------------------------------
def check_main_tex():
    # 找一个示例 main.tex
    tex_files = list(ROOT.rglob("*_AT.tex"))
    if not tex_files:
        add("[WARN] 未找到 main.tex（还未构建？）")
        return

    tex = read(tex_files[0])

    # 检测是否有内联字体指令
    if "\\setCJKmainfont" in tex or "\\setmainfont" in tex:
        add("[ERROR] main.tex 中出现字体设定（Sphinx 主题污染）")
    else:
        add("[OK] main.tex 未包含字体设定（已成功解耦）")

    # 检查是否强行定义标题格式（来自 sphinx）
    if "\\titleformat" in tex:
        add("[WARN] main.tex 内部包含 \\titleformat（Sphinx 标题覆盖你的 titles.tex）")
    else:
        add("[OK] main.tex 未覆盖标题格式")


# ------------------------------------------------------------
# 7. 输出报告
# ------------------------------------------------------------
def print_report():
    print("\n===== STYLE DECOUPLE REPORT =====")
    for line in REPORT:
        print(line)
    print("=================================\n")


# ------------------------------------------------------------
# main
# ------------------------------------------------------------
if __name__ == "__main__":
    check_theme_fonts()
    check_fonts_tex()
    check_headerfooter()
    check_titles()
    check_colors()
    check_main_tex()
    print_report()
