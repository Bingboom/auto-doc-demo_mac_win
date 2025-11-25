@echo off
setlocal enabledelayedexpansion

echo ============================================
echo      Neoway auto-doc build system (Windows)
echo ============================================

:: ---- Detect python ----
where python >nul 2>&1
if %errorlevel%==0 (
    set PYTHON=python
) else (
    where py >nul 2>&1
    if %errorlevel%==0 (
        set PYTHON=py
    ) else (
        echo [ERROR] Python was not found!
        pause
        exit /b 1
    )
)

:: ---- Parse command ----
if "%~1"=="" goto USAGE

if "%~1"=="all"  goto ALL
if "%~1"=="html" goto ALL
if "%~1"=="pdf"  goto ALL

if "%~1"=="build" goto ONE

goto USAGE


:ALL
%PYTHON% tools/build_docs.py
goto END


:ONE
:: Expect PRODUCT=XXX LANG=YYY
for %%A in (%*) do (
    for /f "tokens=1,2 delims==" %%B in ("%%A") do (
        if /I "%%B"=="PRODUCT" set PRODUCT=%%C
        if /I "%%B"=="LANG"     set LANG=%%C
    )
)

if "%PRODUCT%"=="" goto USAGE
if "%LANG%"=="" goto USAGE

%PYTHON% tools/build_docs.py %PRODUCT% %LANG%
goto END


:USAGE
echo.
echo Usage:
echo    make all
echo    make html
echo    make pdf
echo    make build PRODUCT=N706B LANG=zh_cn
echo.
goto END


:END
endlocal
