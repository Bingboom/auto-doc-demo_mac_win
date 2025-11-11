# 📘 Neoway 自动文档构建维护说明

适用版本：Render RST v8.x + Build PDF v7.6 + LaTeX Inject v2.1

---

## 🧩 1. 目录结构总览

```
auto-doc-demo_mac_win/
├── csv-input/
│   └── at_N706B.csv
├── docs/
│   ├── _common/
│   │   ├── _static/              ← logo、背景图等公共资源
│   │   └── templates/            ← Jinja2 模板
│   │       ├── base_page.j2
│   │       ├── command_page.j2
│   │       └── param_table.j2
│   └── N706B/
│       └── source/
│           ├── conf.py
│           ├── index.rst
│           ├── 1/
│           │   ├── index.rst
│           │   └── AT+CMDNAME.rst
│           └── 2/
│               └── ...
└── tools/
    ├── render_rst.py      ← CSV → RST 转换
    ├── build_pdf.py       ← 调用 Sphinx + XeLaTeX 输出 PDF
    └── latex_inject.py    ← 向 conf.py 注入 LaTeX 样式与页眉页脚
```

---

## ⚙️ 2. 构建流程（完整自动化）

### 🪄 一键生成手册

```bash
python tools/build_pdf.py
```

运行后自动执行：

1. **CSV → RST** ：调用 `render_rst.py` 从 `csv-input` 读取命令定义；
2. **RST → LaTeX** ：调用 Sphinx 构建；
3. **LaTeX 注入** ：`latex_inject.py` 修改 `conf.py`，注入页眉、字体、封面；
4. **XeLaTeX 编译** ：自动执行两轮；
5. **输出 PDF** ：最终文件保存到

```
   docs/N706B/build/pdf/Neoway_N706B_AT_命令手册_v1.4.pdf
```

---

## 🧱 3. 各脚本说明

| 文件                | 功能                                                                                             | 关键输出                   |
| ------------------- | ------------------------------------------------------------------------------------------------ | -------------------------- |
| `render_rst.py`   | 从 CSV 渲染章节结构、命令页、索引页                                                              | `/docs/N706B/source/*`   |
| `latex_inject.py` | 在 `conf.py`中插入 LaTeX block，包括：– 字体配置– 页眉/页脚（左logo、右章节标题）– 封面模板 | 直接修改 conf.py           |
| `build_pdf.py`    | 主调度器，依次执行 RST → LaTeX → PDF，兼容 macOS/Windows/Linux                                 | `/docs/N706B/build/pdf/` |

---

## 🖋 4. 模板可修改项

### 📄 command_page.j2

命令页结构模板，可自定义以下段落：

* 功能描述
* 命令格式 / 响应 / 示例
* 参数表格式（嵌套使用 `param_table.j2`）

### 🪶 latex_inject.py 可调节项

* **页眉右上角内容** ：

  目前为 `第X章 章节名`，定义在：

```latex
  \fancyhead[R]{\nouppercase{\chaptername~\thechapter~\leftmark}}
```

* **页脚版权** ：

```latex
  深圳市有方科技股份有限公司版权所有
```

* **封面配色** ：

  改 `\color[HTML]{70AD47}` 即可。

---

## 🧩 5. 常见错误与修复

| 错误提示                                            | 原因                  | 修复方式                                          |
| --------------------------------------------------- | --------------------- | ------------------------------------------------- |
| `SyntaxError: invalid syntax`                     | Python 字符串转义冲突 | 使用最新版 latex_inject.py                        |
| `LaTeX Error: File not found _common/_static/...` | 静态资源未复制        | 检查 `_common/_static`是否存在                  |
| `Command 'xelatex' not found`                     | 系统未安装 XeLaTeX    | macOS:`brew install mactex`Windows: 安装 MiKTeX |
| 页眉未更新章节                                      | Sphinx 缓存旧 conf.py | 删除 `docs/N706B/build/latex`后重试             |
| 页脚页码消失                                        | fancyhdr 样式覆盖冲突 | 确认 `\AtBeginDocument{\pagestyle{normal}}`存在 |

---

## 💡 6. 手动控制部分

如需跳过自动注入，可执行：

```bash
python tools/build_pdf.py --no-inject
```

（需你自行修改 `conf.py` 的 LaTeX block）

---

## ✅ 7. 跨平台说明

| 系统    | 字体配置                            | 是否支持    |
| ------- | ----------------------------------- | ----------- |
| macOS   | PingFang SC + Menlo                 | ✅ 完整支持 |
| Windows | Microsoft YaHei + Consolas          | ✅ 完整支持 |
| Linux   | Noto Sans CJK SC + DejaVu Sans Mono | ✅ 推荐     |

---

## 🧾 8. 版本追踪建议

每次修改模板或 LaTeX 样式，建议：

1. 提交至分支 `pdfXXXX`；
2. 在提交信息中注明模板版本；
3. 标记 `docs/N706B/build/pdf/` 下输出文件对应版本号。

---

> 🧠 小贴士：
>
> 若后续新增模块（如 `英文版文档构建`），可在 `latex_inject.py` 中封装多语言逻辑，通过参数 `lang='en'` 切换。

---

维护人：文档工程组（Neoway）

最后更新：{datetime.now():%Y-%m-%d %H:%M}
