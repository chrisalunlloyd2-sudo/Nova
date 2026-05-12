@echo off
title AI Rolling Autoloader [DIAGNOSTIC MODE]
color 0e
echo ==============================================
echo        AI Rolling Autoloader - DIAGNOSTIC
echo ==============================================
echo.

if "%~1"=="" (
    echo [!] ERROR: No folder detected. 
    echo Please DRAG AND DROP a folder directly onto this icon.
    echo.
    pause
    exit /b
)

echo [1] Verifying Paths...
if not exist "C:\Users\viper\python\python.exe" (
    echo [!] FATAL: python.exe not found at C:\Users\viper\python\
    pause
    exit /b
)
if not exist "C:\Users\viper\rolling_core.py" (
    echo [!] FATAL: rolling_core.py not found at C:\Users\viper\
    pause
    exit /b
)

echo [2] Launching Python Engine...
echo Target: "%~1"
echo.

"C:\Users\viper\python\python.exe" "C:\Users\viper\rolling_core.py" "%~1"

set EXIT_CODE=%ERRORLEVEL%
echo.
echo ==============================================
echo        Execution Finished.
echo        Exit Code: %EXIT_CODE%
echo ==============================================
if %EXIT_CODE% NEQ 0 (
    echo [!] ALERT: The engine returned an error code.
) else (
    echo [*] SUCCESS: Process finished successfully.
)
echo.
echo Press any key to close this window.
pause > nul
