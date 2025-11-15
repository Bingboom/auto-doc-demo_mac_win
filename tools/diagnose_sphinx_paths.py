# tools/diagnose_sphinx_paths.py
from pathlib import Path
import sys
import os
import importlib.util

print("===== 🔍 Sphinx 导入路径诊断 工具 =====\n")

# 1) 项目根目录推断
CURRENT = Path(__file__).resolve()
PROJECT_ROOT = CURRENT.parents[1]
print(f"[1] 当前脚本位置：{CURRENT}")
print(f"[1] 推断项目根目录：{PROJECT_ROOT}")
print("  ✔ 是否存在 .git？", ".git" in [p.name for p in PROJECT_ROOT.iterdir()])
print()

# 2) 检查 conf.py 位置
CONF_PATH = PROJECT_ROOT / "docs" / "N706B" / "source" / "conf.py"
print(f"[2] 检查 conf.py：{CONF_PATH}")
print("  ✔ 是否存在？", CONF_PATH.exists())
print()

# 3) 检查 tools.paths 模块物理位置
TOOLS_DIR = PROJECT_ROOT / "tools"
PATHS_PY = TOOLS_DIR / "paths.py"

print(f"[3] tools 目录：{TOOLS_DIR}")
print("  ✔ 是否存在？", TOOLS_DIR.exists())
print(f"[3] paths.py 文件：{PATHS_PY}")
print("  ✔ 是否存在？", PATHS_PY.exists())
print()

# 4) Sphinx 执行时的 sys.path 模拟
print("[4] 当前 sys.path 前 10 项：")
for p in sys.path[:10]:
    print("   -", p)
print()

# 5) 测试是否能 import tools.paths
print("[5] 测试 import tools.paths ...")

def test_import_tools_paths():
    try:
        spec = importlib.util.find_spec("tools.paths")
        if spec is None:
            print("  ❌ Python 无法找到模块：tools.paths")
        else:
            print("  ✔ spec 找到：", spec.origin)

        # 真正尝试 import
        import tools.paths
        print("  ✔ import 成功！")
        print("  PATHS keys:", list(tools.paths.PATHS.keys()))
    except Exception as e:
        print("  ❌ import 失败：", repr(e))

test_import_tools_paths()
print()

# 6) 模拟 Sphinx 在 conf.py 中 sys.path 需要加入的路径
EXPECTED_PATH = str(PROJECT_ROOT)
print(f"[6] Sphinx 需要加入 sys.path 的路径：{EXPECTED_PATH}")
print("  ✔ 是否在当前 sys.path 中？", EXPECTED_PATH in sys.path)
print()

# 7) 给出修复建议
print("===== 🩹 修复建议 =====")

if not (EXPECTED_PATH in sys.path):
    print("\n👉 你需要在 conf.py 顶部加入：\n")
    print("    import os, sys")
    print("    sys.path.insert(0, os.path.abspath('../../..'))")
    print((f"\n因为你的 conf.py 在：{CONF_PATH}"))
else:
    print("✔ sys.path 配置看起来正常，但 import 仍失败 ->")
    print("  说明你可能在不同路径（Downloads vs Documents）运行导致版本冲突。")

print("\n===== 诊断结束 =====")
