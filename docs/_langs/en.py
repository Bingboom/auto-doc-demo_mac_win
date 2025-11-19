# ====================================
# Language Pack: en
# ====================================

PROJECT_TITLE = "AT Commands Manual"
ISSUE = "1.0"
DATE  = "2025-11-18"

COMPANY_NAME = "Neoway Technology Co., Ltd. All Rights Reserved."
COVER_TITLE_COLOR = "1F4E78"

IS_CHINESE = False
PDF_MAIN_FONT = "Times New Roman"

# ============================
# English chapter formatting
# ============================
CHAPTER_FORMAT = r"""
% Force chapter numbers to Arabic, not ONE/TWO
\renewcommand{\thechapter}{\arabic{chapter}}

\renewcommand{\chaptername}{Chapter}

% --------- 页眉右上角 ---------
\renewcommand{\chaptermark}[1]{%
  \markboth{Chapter \thechapter\ #1}{}%
}

% --------- 章节首页标题（Chapter 1 xxx） ---------
\titleformat{\chapter}
  {\Huge\bfseries}
  {Chapter \thechapter}
  {1em}
  {}
"""
