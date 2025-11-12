@echo off
IF "%1"=="init" (
  py -m pip install -U pip
  py -m pip install -r requirements.txt
  GOTO :eof
)

IF "%1"=="html" (
  py tools\build_docs.py
  GOTO :eof
)

IF "%1"=="pdf" (
  py tools\build_pdf.py
  GOTO :eof
)

IF "%1"=="pdf-no-cover" (
  py tools\build_pdf.py --no-cover
  GOTO :eof
)

echo Usage: make.bat init ^| html ^| pdf ^| pdf-no-cover ^| clean
