# ================================================================
# 📘 Neoway Render RST v7.7 — 稳定完整版（章节+目录修复）
# ================================================================
import pandas as pd
from jinja2 import Environment
from datetime import datetime
from pathlib import Path
import json

# === 注册模板环境，允许使用 max / min / len 等内置函数 ===
env = Environment()
env.globals.update(max=max, min=min, len=len)

# === 项目信息 ===
PROJECT_NAME = "Neoway AT 命令手册"
VERSION = "v1.4"
AUTHOR = "文档工程组"
DATE = datetime.now().strftime("%Y-%m-%d")

# === 路径定义 ===
PROJECT_ROOT = Path.cwd()
for parent in [PROJECT_ROOT] + list(PROJECT_ROOT.parents):
    if (parent / "csv-input").exists():
        PROJECT_ROOT = parent
        break

CSV_PATH = PROJECT_ROOT / "csv-input" / "at_N706B.csv"
ROOT_DIR = PROJECT_ROOT / "docs" / "N706B" / "source"
OUTPUT_DIR = ROOT_DIR
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# === 读取 CSV ===
df = pd.read_csv(CSV_PATH, dtype=str).fillna("")

# === 按章节分组 ===
chapters = []
for chap, group in df.groupby("章节", sort=True):
    chap_name = group["章节名称"].iloc[0].strip() or f"第{chap}章"
    chapters.append((chap, chap_name, group))

# === 模板：主 index.rst ===
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

# === 模板：章节 index.rst ===
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

# === 模板：单命令页 ===
cmd_tmpl = env.from_string(r"""
.. _cmd-{{ cmd_name|lower }}:

{{ cmd_name }}：{{ cmd_title }}
{{ "-" * max((cmd_name|length + cmd_title|length + 2), 10) }}

{{ desc }}

命令格式
^^^^^^^^
{% set formats = cmd_format.split(';') if ';' in cmd_format else [cmd_format] %}
{% for f in formats %}
{% set f_clean = f.strip() %}
{% if f_clean %}
**{{ ["执行命令", "查询命令", "测试命令", "设置命令"][loop.index0] if loop.index0 < 4 else "命令" }}**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**命令：**

::

    {{ f_clean }}

**响应：**

::

{% if cmd_response.strip() %}
    {{ cmd_response.strip().replace('\n', '\n    ') }}
{% else %}
    OK
{% endif %}

{% endif %}
{% endfor %}

参数
^^^^
{% if params %}
{% for k, v in params.items() %}
- **{{ k }}**：
  
    {{ v.get('__desc__', '') }}
{% if v.get('__options__') %}
{% for opt, text in v['__options__'].items() %}
    - {{ opt }}：{{ text }}
{% endfor %}
{% endif %}
{% endfor %}
{% else %}
(无参数)
{% endif %}

说明
^^^^
{{ note.strip() if note else "(无说明)" }}

示例命令
^^^^^^^^

::

{% if example.strip() %}
    {{ example.strip().replace('\n', '\n    ') }}
{% else %}
    （无示例）
{% endif %}
""".strip())

# === 渲染章节 ===
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
