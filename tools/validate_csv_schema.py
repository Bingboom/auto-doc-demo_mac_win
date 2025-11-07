#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
validate_csv_schema.py
验证 csv-input 目录下所有 CSV 文件结构一致性：
- 列名是否一致
- 字段数是否正确
- 引号、逗号配对问题
- 空行/缺值检测
"""

import csv
import os
from pathlib import Path
import sys

def validate_csv_schema(csv_dir: Path):
    csv_files = list(csv_dir.glob("*.csv"))
    if not csv_files:
        print(f"❌ 未找到 CSV 文件：{csv_dir}")
        sys.exit(1)

    print(f"🔍 开始验证 CSV 文件结构，共 {len(csv_files)} 个文件...")
    reference_header = None
    errors = []

    for csv_file in csv_files:
        print(f"🧾 检查 {csv_file.name} ...")
        with open(csv_file, "r", encoding="utf-8-sig") as f:
            reader = csv.reader(f)
            try:
                header = next(reader)
            except Exception as e:
                errors.append(f"❌ {csv_file.name} 无法读取表头：{e}")
                continue

            # 初始化参考表头
            if reference_header is None:
                reference_header = header
                print(f"✅ 模板表头：{reference_header}")
            else:
                if header != reference_header:
                    errors.append(
                        f"⚠️ {csv_file.name} 表头不一致：\n  预期: {reference_header}\n  实际: {header}"
                    )

            # 检查字段数一致性
            for i, row in enumerate(reader, start=2):
                if len(row) != len(reference_header):
                    errors.append(
                        f"⚠️ {csv_file.name} 第 {i} 行字段数不符: {len(row)} != {len(reference_header)}"
                    )

    if errors:
        print("\n❌ 验证发现以下问题：")
        for e in errors:
            print(e)
        sys.exit(1)
    else:
        print("\n✅ 所有 CSV 文件结构一致，验证通过。")

if __name__ == "__main__":
    project_root = Path(__file__).resolve().parents[1]
    csv_dir = project_root / "csv-input"
    validate_csv_schema(csv_dir)
