# Quick Start Development Script for SentiPort

Write-Host "
╔═══════════════════════════════════════════════════════════╗
║     SentiPort - Development Environment Setup            ║
╚═══════════════════════════════════════════════════════════╝
" -ForegroundColor Cyan

# Navigate to project
$projectPath = "C:\Users\HARIHARAN\Projects\SentiPort"
if (-not (Test-Path $projectPath)) {
    Write-Host "❌ Project not found at $projectPath" -ForegroundColor Red
    exit 1
}

Set-Location $projectPath
Write-Host "✅ Project directory: $projectPath" -ForegroundColor Green

# Check Node.js
Write-Host ""
Write-Host "🔍 Checking Node.js..." -ForegroundColor Yellow
$nodeVersion = node --version
if ($?) {
    Write-Host "✅ Node.js $nodeVersion found" -ForegroundColor Green
} else {
    Write-Host "❌ Node.js not found. Install from https://nodejs.org" -ForegroundColor Red
    exit 1
}

# Check npm
Write-Host ""
Write-Host "🔍 Checking npm..." -ForegroundColor Yellow
$npmVersion = npm --version
if ($?) {
    Write-Host "✅ npm $npmVersion found" -ForegroundColor Green
} else {
    Write-Host "❌ npm not found" -ForegroundColor Red
    exit 1
}

# Install dependencies
Write-Host ""
Write-Host "📦 Installing dependencies..." -ForegroundColor Yellow
Write-Host "⏳ This may take 2-3 minutes..." -ForegroundColor Cyan
npm install

if ($?) {
    Write-Host "✅ Dependencies installed!" -ForegroundColor Green
} else {
    Write-Host "❌ Installation failed" -ForegroundColor Red
    exit 1
}

# Start development server
Write-Host ""
Write-Host "🚀 Starting development server..." -ForegroundColor Yellow
Write-Host ""
Write-Host "⏳ Server starting on http://localhost:5173" -ForegroundColor Cyan
Write-Host ""
Write-Host "When you see 'VITE v5' message, your app is ready!" -ForegroundColor Green
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor White
Write-Host ""

npm run dev
