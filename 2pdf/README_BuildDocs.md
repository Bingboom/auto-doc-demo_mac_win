# 🏗️ Neoway Auto Documentation System — 企业构建说明

本工程用于自动从 CSV → RST → LaTeX → PDF 生成  **AT 命令手册**。
项目支持多型号（xxx等），统一使用 `_common` 公共配置。

---

## 📁 项目结构

auto-doc-demo_mac_win/
├── tools/
│   ├── build_pdf.py         # 主构建入口（企业版 v8.0）
│   ├── latex_inject.py      # 自动注入 LaTeX 模板（企业版 v3.6）
│   ├── render_rst.py        # CSV → RST 转换工具
├── docs/
│   ├── _common/
│   │   ├── conf_common.py   # 全局公司参数、字体、版权信息
│   │   └── _static/         # 封面图、Logo、页眉图片
│   ├── N706B/
│   │   └── source/
│   │       └── conf.py      # 项目配置（自动注入）
│   └── N725/ ...
└── csv-input/
    └── at_N706B.csv         # 命令定义源数据

---

## ⚙️ 环境要求

- **Python 3.9+**
- pip 包：
  bash
  pip install sphinx==7.4.7 sphinx-rtd-theme jinja2 pandas
- 系统需安装 **XeLaTeX**

  - macOS: 安装 [MacTeX](https://tug.org/mactex/)
  - Windows: 安装 [TeX Live](https://www.tug.org/texlive/)

---

## 🚀 一键构建

在仓库根目录执行：

bash
python tools/build_pdf.py

执行顺序如下：

1. 自动注入 LaTeX 样式 → 更新 `docs/N706B/source/conf.py`
2. 运行 `sphinx-build` 构建 LaTeX 源文件
3. 自动运行两轮 `xelatex` 编译
4. 输出 PDF 到：

   docs/N706B/build/pdf/Neoway_N706B_AT_命令手册_V1.4.pdf

---

## 🖋️ LaTeX 模板说明

- 封面背景： `_common/_static/background.png`
- 页眉 Logo： `_common/_static/header-logo.png`
- 左页脚： `深圳市有方科技股份有限公司版权所有`
- 页眉右上角： `第 2 章 SMS命令`

所有字体与版式在 `_common/conf_common.py` 中统一配置：

python
zh_font = "PingFang SC"       # macOS
mono_font = "Menlo"           # macOS
company = "深圳市有方科技股份有限公司"

---

## 🧩 模块化扩展

未来新增型号（如 N725）只需：

1. 在 `docs/N725/source/` 中创建 `conf.py`（复制 N706B 的版本）
2. 修改型号名与 CSV 文件路径
3. 直接执行 `python tools/build_pdf.py` 即可生成 PDF

---

## 🧰 常见问题

| 问题                                      | 原因             | 解决方法                                |
| ----------------------------------------- | ---------------- | --------------------------------------- |
| `NameError: latex_elements not defined` | conf.py 未初始化 | 确保 conf.py 含 `latex_elements = {}` |
| 页眉章节号错误                            | 旧模板未更新     | 重新执行 `build_pdf.py` 注入新模板    |
| PDF 不生成                                | XeLaTeX 编译失败 | 检查 LaTeX 日志，确认字体存在           |

---

## 📄 版权声明

> 💡 小贴士：每次构建都会自动更新注入时间戳，便于版本追踪。
