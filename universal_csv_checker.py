#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
universal_csv_checker.py — CSV 格式检查器（不修改原文件）
检查内容：
1. 行字段数是否与第一行一致
2. 是否存在额外逗号、缺少引号闭合等问题
3. 打印出问题行号、行内容与字段数
"""

import csv
import sys
from pathlib import Path

def check_csv(csv_file):
    print(f"\n📄 正在检查: {csv_file}")
    csv_file = Path(csv_file)

    if not csv_file.exists():
        print("❌ 文件不存在！")
        return

    # 尝试读取 CSV（不改内容）
    with csv_file.open("r", encoding="utf-8", errors="replace") as f:
        lines = f.readlines()

    # 尝试用 Python csv.reader 解析，但保留原始错误
    print("🔍 扫描 CSV 格式...\n")

    reader = csv.reader(lines)
    expected_cols = None
    ok = True

    for i, row in enumerate(reader, start=1):
        col_count = len(row)

        # 第一行决定列数
        if expected_cols is None:
            expected_cols = col_count
            print(f"📌 第一行列数 = {expected_cols}")
            continue

        # 比对列数
        if col_count != expected_cols:
            ok = False
            print(f"❌ 第 {i} 行列数不一致: {col_count} 列（期望 {expected_cols} 列）")
            raw_line = lines[i-1].rstrip()
            print(f"   原始行内容: {raw_line}")

    if ok:
        print("✔ CSV 结构正常，没有检测到列数问题。")
    else:
        print("\n⚠ 请手动检查标出的行（多半是多余的逗号、换行、引号导致）。")



if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python universal_csv_checker.py path/to/file.csv")
        sys.exit(1)

    check_csv(sys.argv[1])
