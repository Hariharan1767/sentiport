@echo off
REM Sentiport API Server - Universal Launcher
REM Uses py.exe (Python launcher) to start the API server

setlocal enabledelayedexpansion
cd /d "%~dp0"

echo ================================
echo Sentiport API Server
echo ================================
echo.

REM Try to find and use venv first
if exist ".venv\Scripts\python.exe" (
    set PYTHON_CMD=.\.venv\Scripts\python.exe
    echo Using Virtual Environment Python
    goto check_flask
)

REM Fall back to py.exe (Python launcher)
where py.exe >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found!
    echo Please install Python from https://www.python.org/downloads/
    pause
    exit /b 1
)

set PYTHON_CMD=py.exe
echo Using System Python

:check_flask
echo Checking dependencies...
%PYTHON_CMD% -m pip list 2>nul | findstr /i flask >nul
if errorlevel 1 (
    echo Flask not installed. Installing dependencies...
    %PYTHON_CMD% -m pip install --upgrade pip -q
    %PYTHON_CMD% -m pip install -r requirements.txt -q
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies
        pause
        exit /b 1
    )
)

echo.
echo ================================
echo Starting API Server...
echo ================================
echo.
echo API: http://localhost:5000
echo Health: http://localhost:5000/api/health
echo.
echo Press Ctrl+C to stop
echo.

%PYTHON_CMD% api_server.py

pause
