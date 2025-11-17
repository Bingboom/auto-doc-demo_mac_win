@echo off
set PY=python

echo Neoway auto-doc build system

if "%1"=="all" goto ALL
if "%1"=="html" goto ALL
if "%1"=="pdf" goto ALL

if "%1"=="build" goto ONE

echo Usage:
echo    make all
echo    make html
echo    make pdf
echo    make build PRODUCT=N706B LANG=zh_CN
goto END


:ALL
%PY% tools/build_docs.py
goto END


:ONE
%PY% tools/build_docs.py %PRODUCT% %LANG%
goto END


:END
