# ================================================================
# 📘 Neoway Render RST v8.0 — 模板外置版（修复重复命令格式问题）
# ================================================================
import pandas as pd
from jinja2 import Environment, FileSystemLoader
from datetime import datetime
from pathlib import Path
import json

# === 基本项目信息 ===
PROJECT_NAME = "Neoway AT 命令手册"
VERSION = "v1.4"
AUTHOR = "文档工程组"
DATE = datetime.now().strftime("%Y-%m-%d")

# === 定位项目根目录 ===
PROJECT_ROOT = Path.cwd()
for parent in [PROJECT_ROOT] + list(PROJECT_ROOT.parents):
    if (parent / "csv-input").exists():
        PROJECT_ROOT = parent
        break

# === 路径定义 ===
CSV_PATH = PROJECT_ROOT / "csv-input" / "at_N706B.csv"
ROOT_DIR = PROJECT_ROOT / "docs" / "N706B" / "source"
OUTPUT_DIR = ROOT_DIR
TEMPLATE_DIR = PROJECT_ROOT / "docs" / "_common" / "templates"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# === 模板加载环境 ===
env = Environment(loader=FileSystemLoader(str(TEMPLATE_DIR)))
env.globals.update(max=max, min=min, len=len)

# === 加载模板 ===
main_index_tmpl = env.from_string("""
{{ project_name }} {{ version }}
{{ "=" * (project_name|length + version|length + 1) }}

:Author: {{ author }}
:Date: {{ date }}
:Version: {{ version }}

.. toctree::
   :maxdepth: 1
   :titlesonly:

{% for chap in chapters %}
   {{ chap[0] }}/index
{% endfor %}

附录
----
.. toctree::
   :maxdepth: 1
   :titlesonly:

   appendix/abbreviations
   appendix/index
""".strip())

chapter_index_tmpl = env.from_string("""
第{{ chap_num }}章 {{ chap_name }}
{{ "=" * max((chap_name|length + 6), 10) }}

.. toctree::
   :maxdepth: 1
   :titlesonly:

{% for cmd in cmds %}
   {{ cmd }}
{% endfor %}
""".strip())

# === 外部命令页模板（修复重复命令格式）===
cmd_tmpl = env.get_template("command_page.j2")

# === 读取 CSV 数据 ===
df = pd.read_csv(CSV_PATH, dtype=str).fillna("")

# === 按章节分组 ===
chapters = []
for chap, group in df.groupby("章节", sort=True):
    chap_name = group["章节名称"].iloc[0].strip() or f"第{chap}章"
    chapters.append((chap, chap_name, group))

# === 渲染每个章节 ===
for chap_num, chap_name, group in chapters:
    chap_dir = OUTPUT_DIR / str(chap_num)
    chap_dir.mkdir(parents=True, exist_ok=True)

    cmd_list = []
    for _, row in group.iterrows():
        cmd_name = row["命令"].strip()
        cmd_title = row["命令标题"].strip()
        cmd_file = chap_dir / f"{cmd_name}.rst"
        cmd_list.append(cmd_name)

        try:
            params = json.loads(row["参数json"])
        except Exception:
            params = {}

        rendered = cmd_tmpl.render(
            cmd_name=cmd_name,
            cmd_title=cmd_title,
            desc=row["功能描述"],
            cmd_format=row["命令格式"],
            cmd_response=row["响应"],
            params=params,
            note=row.get("备注", ""),
            example=row.get("示例命令", ""),
        )

        cmd_file.write_text(rendered.strip() + "\n", encoding="utf-8")
        print(f"✅ 已生成命令：{cmd_name}")

    # === 渲染章节 index ===
    idx_path = chap_dir / "index.rst"
    idx_render = chapter_index_tmpl.render(
        chap_num=chap_num,
        chap_name=chap_name,
        cmds=cmd_list
    )
    idx_path.write_text(idx_render.strip() + "\n", encoding="utf-8")
    print(f"📘 第{chap_num}章 {chap_name} 生成完成（{len(cmd_list)} 条命令）")

# === 渲染主 index.rst ===
main_rst = main_index_tmpl.render(
    project_name=PROJECT_NAME,
    version=VERSION,
    author=AUTHOR,
    date=DATE,
    chapters=chapters
)
(OUTPUT_DIR / "index.rst").write_text(main_rst.strip() + "\n", encoding="utf-8")
print(f"🎯 主 index.rst 生成完成 → {OUTPUT_DIR/'index.rst'}")
