# -*- coding: utf-8 -*-
"""
🧩 latex_inject.py — 安全稳定版 LaTeX 样式注入脚本（2025-11）
------------------------------------------------------------
功能：
1. 自动检测并清理 UTF-8 BOM
2. 自动备份 conf.py
3. 安全更新或插入 latex_elements 段
4. 使用非贪婪匹配 + lambda 防止 re.sub 误解析反斜杠
5. 幂等（重复执行不会破坏 conf.py）
6. 可独立运行，也可由 build_pdf.py 调用
"""

from pathlib import Path
import re
import shutil
import time
import sys


# ====== 基本路径 ======
BASE = Path(__file__).resolve().parents[1]
CONF_PATH = BASE / "docs" / "N706B" / "source" / "conf.py"


# ====== 通用 BOM 检测与清理 ======
def remove_bom(file_path: Path):
    """检测并移除 UTF-8 BOM"""
    try:
        if not file_path.exists():
            return
        data = file_path.read_bytes()
        if data.startswith(b"\xef\xbb\xbf"):
            print(f"⚠️ 检测到 BOM，已清理：{file_path}")
            file_path.write_bytes(data[3:])
    except Exception as e:
        print(f"❌ remove_bom 失败: {e}")


# ====== 文件读写 ======
def read_conf(path: Path) -> str:
    remove_bom(path)
    return path.read_text(encoding="utf-8")


def write_conf(path: Path, content: str):
    path.write_text(content, encoding="utf-8")
    remove_bom(path)


# ====== 备份文件 ======
def backup_file(path: Path):
    if not path.exists():
        return
    ts = time.strftime("%Y%m%d%H%M%S")
    bak_path = path.with_suffix(path.suffix + f".bak.{ts}")
    shutil.copy2(path, bak_path)
    print(f"💾 已备份 {path} -> {bak_path}")


# ====== 核心函数：注入 LaTeX 样式 ======
def inject_latex_style(conf_path: Path):
    """在 conf.py 中插入或更新 latex_elements 设置"""
    conf_text = read_conf(conf_path)

    # --- LaTeX 样式块 ---
    latex_block = '''
latex_elements = {
    "papersize": "a4paper",
    "pointsize": "11pt",
    "preamble": r"""
\\usepackage{xeCJK}
\\setCJKmainfont{SimSun}
\\setCJKmonofont{SimSun}
\\setCJKsansfont{SimHei}
\\usepackage{fancyhdr}
\\pagestyle{fancy}
\\fancyhead[L]{\\textbf{Neoway 文档工程组}}
\\fancyhead[R]{\\textbf{N706B AT 命令手册}}
\\fancyfoot[L]{Neoway Technology Co., Ltd. 版权所有}
\\fancyfoot[R]{\\thepage}
""",
}
'''.strip()

    # === 备份 ===
    backup_file(conf_path)

    # ✅ 改进点：精确匹配单个 latex_elements 块，防止误吞其他 {}
    pattern = re.compile(
        r"(?ms)^latex_elements\s*=\s*\{.*?\}\n(?=^[A-Za-z_]|$)",
        flags=re.MULTILINE,
    )

    if re.search(pattern, conf_text):
        print("🔁 检测到 latex_elements，执行更新 …")
        conf_text = re.sub(pattern, lambda m: latex_block + "\n", conf_text)
    else:
        print("➕ 未检测到 latex_elements，插入新的配置到文件末尾 …")
        conf_text = conf_text.rstrip() + "\n\n" + latex_block + "\n"

    # === 写入文件 ===
    write_conf(conf_path, conf_text)
    print(f"✅ 已更新 {conf_path}")


# ====== 主入口 ======
def main():
    print("🧩 Step 1: 注入 LaTeX 样式 …")
    try:
        inject_latex_style(CONF_PATH)
        print("✅ LaTeX 样式注入完成。")
    except FileNotFoundError as e:
        print(f"❌ 错误: {e}")
        sys.exit(2)
    except Exception as e:
        print(f"❌ 未知错误: {e}")
        sys.exit(3)


if __name__ == "__main__":
    main()
