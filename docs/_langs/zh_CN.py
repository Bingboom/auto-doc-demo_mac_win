# ====================================
# Language Pack: zh_CN
# ====================================

PROJECT_TITLE = "AT命令手册"
ISSUE = "1.0"
DATE  = "2025-11-18"

COMPANY_NAME = "深圳市有方科技股份有限公司 版权所有"
COVER_TITLE_COLOR = "70AD47"

IS_CHINESE = True
PDF_MAIN_FONT = "SimSun"

# ============================
# 中文章节标题布局
# ============================
CHAPTER_FORMAT = r"""
\renewcommand{\chaptername}{}

% ------- 中文页眉右上角格式 -------
\renewcommand{\chaptermark}[1]{%
  \markboth{第\thechapter 章\ #1}{}%
}

% ------- 章节首页标题（第1章 …） -------
\titleformat{\chapter}
  {\Huge\bfseries}
  {第\thechapter 章}
  {1em}
  {}
"""
