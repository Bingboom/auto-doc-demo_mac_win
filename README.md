```markdown
# auto-doc-demo_mac_win

> 学习型示例仓库：用 **“继承与覆盖（Inheritance & Override）”** 的方式，结构化实现  
> **Word/CSV → RST → Sphinx → HTML/PDF** 的企业级技术文档构建流程（macOS / Windows）。

本仓库不是“一次性脚本”，而是**可复用、可扩展**的分层代码范式：  
- 公共配置与工具放在“公共层”，  
- 语言/项目/版本在“业务层”仅做**最小覆写**，  
- 构建脚本将参数**层层下传**，最终驱动 Sphinx 构建。

---

## ✨ 你能学到什么

- 如何用 **Python 模块导入** + **变量覆盖** 组织 Sphinx `conf.py`  
- 如何用 **Jinja2 模板继承** 保持文档页结构一致，同时局部改动  
- 如何把 **构建脚本** 做成“公共框架 + 轻量覆写”的可拓展体系  
- 如何在 **macOS/Windows** 使用同一套目录和命令

---

## 🧱 目录结构（示例）

> 以学习为主，真实仓库命名可能略有不同；保持**同等分层**即可。

```

.
├─ conf_docs/                 # 配置分层（公共 → 语言/产品 → 版本）
│  ├─ common_conf.py          # 公共 Sphinx 配置（主题、扩展、全局选项）
│  ├─ zh_CN_conf.py           # 覆盖：中文站点（继承 common_conf）
│  ├─ en_conf.py              # 覆盖：英文站点（继承 common_conf）
│  └─ product_n706/           # （可选）按产品再分一层
│     ├─ base_conf.py         # 产品公共配置
│     └─ zh_CN_conf.py        # 产品中文配置（最终作为 -c 传入）
│
├─ templates/                 # 模板分层（Jinja2 / RST）
│  ├─ base/                   # 基础页框架：layout、章节索引、命令页骨架
│  ├─ blocks/                 # 可复用片段：参数表、注意事项、示例代码块
│  └─ overrides/              # 按主题/项目的小范围覆写
│
├─ themes/                    # 主题分层（可选：在 RTD/Book/Material 之上覆写）
│  ├─ base_theme/             # 继承上游主题
│  └─ custom/                 # 局部 CSS/JS 覆写（后加载）
│
├─ docs/
│  ├─ zh_CN/source/           # RST 源（由 CSV/模板生成或手写）
│  ├─ zh_CN/build/            # 输出（HTML/PDF）
│  ├─ en/source/
│  └─ en/build/
│
├─ tools/                     # 构建工具分层（公共 → 业务覆写）
│  ├─ build_docs.py           # 通用构建入口（解析参数并调用 sphinx-build）
│  ├─ gen_rst.py              # CSV→RST 渲染器（Jinja2：模板 + 数据）
│  ├─ cli.py                  # 命令行封装（Windows/macOS 统一）
│  └─ adapters/               # 针对不同数据源的适配器（CSV/JSON/表格平台）
│
├─ data/                      # 示例数据（CSV/JSON）
│  └─ at_commands.csv
│
├─ requirements.txt
└─ README.md

````

---

## ⚙️ 环境准备

### macOS
```bash
# 建议 Python 3.10+（或你的团队标准版本）
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
````

### Windows (PowerShell)

```powershell
python -m venv .venv
. .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

> PDF 构建需 LaTeX 发行版（可选）：macOS 推荐 MacTeX，Windows 推荐 MiKTeX/TeX Live。

---

## 🚀 常用命令

### 1) 生成 RST（从 CSV/JSON 等）

```bash
python tools/gen_rst.py \
  --input data/at_commands.csv \
  --template templates/base/command_page.rst.j2 \
  --outdir docs/zh_CN/source/commands
```

### 2) 构建 HTML

```bash
# 直接传入要使用的配置层（可为 conf_docs/zh_CN_conf.py 或产品层）
python tools/build_docs.py \
  --conf conf_docs/zh_CN_conf.py \
  --sourcedir docs/zh_CN/source \
  --outdir docs/zh_CN/build/html \
  --builder html
```

### 3) 构建 PDF（如需）

```bash
python tools/build_docs.py \
  --conf conf_docs/zh_CN_conf.py \
  --sourcedir docs/zh_CN/source \
  --outdir docs/zh_CN/build/pdf \
  --builder latexpdf
```

---

## 🧠 “继承与覆盖”——三个层面的最小示例

### ① 配置层（Sphinx `conf.py`）

```python
# conf_docs/common_conf.py
project = "Neoway Docs"
author = "Neoway"
extensions = [
    "sphinx_rtd_theme",
    "sphinx_copybutton",
]
html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
```

```python
# conf_docs/zh_CN_conf.py
from .common_conf import *        # ① 继承公共配置
language = "zh_CN"                # ② 覆盖：语言
project = "有方科技文档中心"        # ③ 覆盖：项目显示名
html_title = f"{project}"         # ④ 覆盖：站点标题
```

> 规则：**后导入/后定义** 覆盖 **先导入/先定义**；保持**尽可能少的覆写**。

---

### ② 模板层（Jinja2 for RST）

```jinja2
{# templates/base/page.rst.j2 #}
{% block title %}{{ page_title }}{% endblock %}

{% block body %}
{{ content }}
{% endblock %}
```

```jinja2
{# templates/overrides/command_page.rst.j2 #}
{% extends "base/page.rst.j2" %}

{% block title %}{{ cmd.name }} — {{ cmd.title }}{% endblock %}

{% block body %}
{{ super() }}  {# 继承父区块内容 #}

.. note::
   {{ cmd.description }}

**语法**
::
   {{ cmd.syntax }}

**参数**
{% for p in cmd.params %}
- ``{{ p.name }}``: {{ p.desc }}
{% endfor %}
{% endblock %}
```

---

### ③ 构建层（Python 脚本）

```python
# tools/build_docs.py
import subprocess, argparse

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--conf", required=True)
    ap.add_argument("--sourcedir", required=True)
    ap.add_argument("--outdir", required=True)
    ap.add_argument("--builder", default="html")
    args = ap.parse_args()

    cmd = [
        "sphinx-build",
        "-b", args.builder,
        "-c", "conf_docs",       # 让 Sphinx 在此目录查找 conf（或使用 -D 传参）
        args.sourcedir,
        args.outdir
    ]
    # 通过环境变量/参数把具体 conf 告诉 Sphinx
    # 方式 A：在 sourcedir 放一个最薄的 conf.py，内部 `from ... import *`
    # 方式 B：用 -D 覆盖关键项（如 language/html_title 等）
    print(" ".join(cmd))
    subprocess.check_call(cmd)

if __name__ == "__main__":
    main()
```

> 思路：**tools 层不写死业务逻辑**，只负责把“公共规则 + 少量覆写”组合起来执行。

---

## ➕ 如何扩展一个“新产品 / 新语言 / 新版本”

**以“新增英文版 N706 文档”为例：**

1. **复制配置层**

   * `conf_docs/product_n706/base_conf.py`（公共）
   * 新建 `conf_docs/product_n706/en_conf.py`：

     ```python
     from .base_conf import *
     from ..en_conf import *        # 继承全局英文站点设置
     project = "N706 AT Command Manual"
     html_title = project
     ```
2. **准备源文件**

   * 把渲染出的 RST 放到 `docs/en/source/n706/`（或保持你的既定结构）
3. **执行构建**

   ```bash
   python tools/build_docs.py \
     --conf conf_docs/product_n706/en_conf.py \
     --sourcedir docs/en/source \
     --outdir docs/en/build/html \
     --builder html
   ```

> 复用最大化：**公共层一次定义**，业务层只做**几行覆写**。

---

## 🧰 约定与风格

* **命名**：`common_*` 为公共；`*_conf.py` 为覆盖层；`base_*` 为产品内公共
* **模板**：`base/` 放骨架；`blocks/` 放可复用片段；`overrides/` 做局部替换
* **CSS/JS**：后加载的文件用于**覆盖**前面的样式；尽量避免直接改上游主题
* **构建**：所有脚本不要写死路径，用参数/环境变量注入

---

## 🧪 验证清单（快速判断分层是否生效）

* [ ] 改动 `common_conf.py` 会同时影响中/英文两个站点
* [ ] 在 `zh_CN_conf.py` 改 `html_title`，仅中文站点变化
* [ ] 替换 `templates/overrides/command_page.rst.j2`，命令页布局变更但不影响其它模板
* [ ] 新加一个产品层 `product_xxx/base_conf.py`，其它产品无副作用

---

## ❓FAQ / Troubleshooting

* **PDF 构建失败（LaTeX 相关）**
  安装/更新本地 LaTeX 发行版；中文字体用 `xelatex` 并在 `conf.py` 指定字体族。
* **主题样式不生效**
  确认 custom CSS/JS 是否**在主题之后加载**；浏览器硬刷新清缓存。
* **CSV→RST 字段对不齐**
  用 `tools/adapters` 做一层字段映射与校验；在渲染前先打印出中间 JSON 以便定位。
* **Windows 路径问题**
  优先使用 `pathlib`；命令行参数避免反斜杠转义问题。

---

## 📄 许可证

MIT（示例学习用途，可自由复制与修改）

---

## 👤 Maintainer

* 唐夏冰

