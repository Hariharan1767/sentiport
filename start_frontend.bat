@echo off
REM Start Sentiport Frontend - Local Development
REM This script starts the React dev server with Vite

setlocal enabledelayedexpansion
cd /d "%~dp0"

echo ================================
echo Sentiport Frontend - Local Development
echo ================================
echo.

REM Check if node_modules exists
if not exist "node_modules" (
    echo Installing dependencies...
    call npm install
)

REM Start the dev server
echo.
echo Starting Frontend Dev Server...
echo ================================
echo Frontend: http://localhost:5173
echo API: http://localhost:5000
echo ================================
echo.
echo Press Ctrl+C to stop the server
echo.

call npm run dev
