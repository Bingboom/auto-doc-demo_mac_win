# -*- coding: utf-8 -*-
"""
🧩 clean_conf_duplicates.py — 自动清理 LaTeX 样式重复注入
------------------------------------------------------------
功能：
1. 遍历并删除 conf.py 中多余的 LaTeX 注入段
2. 防止不小心注入多次造成语法错误
"""

from pathlib import Path
import re
import sys

# ====== 基本路径 ======
BASE = Path(__file__).resolve().parents[1]
CONF_PATH = BASE / "docs" / "N706B" / "source" / "conf.py"


# ====== 删除重复的 latex_elements 块 ======
def clean_conf(conf_path: Path):
    try:
        conf_text = conf_path.read_text(encoding="utf-8")
        
        # 正则匹配所有 latex_elements 配置块
        pattern = re.compile(r"(?ms)^latex_elements\s*=\s*\{.*?\}\n", flags=re.MULTILINE)
        
        # 替换掉所有重复的 latex_elements 配置块，保留第一个
        cleaned_conf = re.sub(pattern, "", conf_text, count=1)

        # 如果修改过文件，保存更新
        if cleaned_conf != conf_text:
            print(f"🧹 清理了重复的 LaTeX 配置：{conf_path}")
            conf_path.write_text(cleaned_conf, encoding="utf-8")
        else:
            print(f"✅ 没有检测到重复 LaTeX 配置：{conf_path}")

    except Exception as e:
        print(f"❌ 清理失败: {e}")
        sys.exit(2)


# ====== 主入口 ======
if __name__ == "__main__":
    clean_conf(CONF_PATH)
    print("✅ 清理完成。")
