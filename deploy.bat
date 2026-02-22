@echo off
REM Deployment script for Sentiport (Windows)

setlocal enabledelayedexpansion

echo ================================
echo Sentiport Deployment Script
echo ================================
echo.

REM Check prerequisites
echo [1/6] Checking prerequisites...
docker --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Docker is not installed!
    exit /b 1
)
docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Docker Compose is not installed!
    exit /b 1
)
echo [OK] Docker and Docker Compose found
echo.

REM Build images
echo [2/6] Building Docker images...
call docker-compose build
if errorlevel 1 (
    echo ERROR: Failed to build images
    exit /b 1
)
echo [OK] Docker images built
echo.

REM Stop existing containers
echo [3/6] Stopping existing containers...
call docker-compose down 2>nul
echo [OK] Containers stopped
echo.

REM Start services
echo [4/6] Starting services...
call docker-compose up -d
if errorlevel 1 (
    echo ERROR: Failed to start services
    exit /b 1
)
echo [OK] Services started
echo.

REM Wait for services to be healthy
echo [5/6] Waiting for services to be healthy...
set max_attempts=30
set attempt=1

:health_check_loop
if !attempt! gtr !max_attempts! (
    echo ERROR: API health check failed after !max_attempts! attempts
    exit /b 1
)

curl -f http://localhost:5000/api/health >nul 2>&1
if !errorlevel! equ 0 (
    echo [OK] API is healthy
    goto health_check_success
)

echo Attempt !attempt!/!max_attempts!: Waiting for API...
timeout /t 2 /nobreak
set /a attempt=!attempt!+1
goto health_check_loop

:health_check_success
echo.

REM Display deployment summary
echo [6/6] Deployment Summary
echo ================================
echo API Server:      http://localhost:5000
echo Frontend:        http://localhost
echo API Health:      http://localhost:5000/api/health
echo.
echo To view logs:    docker-compose logs -f
echo To stop:         docker-compose down
echo.
echo [OK] Deployment complete!
echo.

endlocal
