@echo off
REM SentiPort - Start All Services
REM Starts Flask API (port 5000) + Vite frontend (port 5173)

setlocal enabledelayedexpansion
cd /d "%~dp0"

echo ================================
echo  SentiPort - Local Deployment
echo ================================
echo.

REM Detect venv folder (supports both .venv and venv)
set VENV_ACTIVATE=
if exist "venv\Scripts\activate.bat"  set VENV_ACTIVATE=venv\Scripts\activate.bat
if exist ".venv\Scripts\activate.bat" set VENV_ACTIVATE=.venv\Scripts\activate.bat

if "%VENV_ACTIVATE%"=="" (
    echo ERROR: No virtual environment found.
    echo Please run:  python -m venv venv
    echo Then:        venv\Scripts\activate
    echo Then:        pip install -r requirements.txt
    pause
    exit /b 1
)

if not exist "node_modules" (
    echo Installing Node dependencies...
    call npm install
)

echo Starting Flask API Server (port 5000)...
start "SentiPort API" cmd /k "call %VENV_ACTIVATE% && python api_server.py"

timeout /t 2 /nobreak > nul

echo Starting Vite Frontend (port 5173)...
start "SentiPort Frontend" cmd /k "npm run dev"

echo.
echo ================================
echo  Services Starting...
echo ================================
echo.
echo  Frontend:  http://localhost:5173
echo  API:       http://localhost:5000/api
echo  Health:    http://localhost:5000/api/health
echo.
echo Press any key to close this launcher window.
echo (Servers will keep running in their own windows)
pause > nul
