# SentiPort Git Setup Script
# This script initializes Git and prepares for GitHub connection

param(
    [string]$GitName = "Your Name",
    [string]$GitEmail = "your.email@example.com"
)

$gitPath = "C:\Program Files\Git\bin\git.exe"

function Run-Git {
    param([string[]]$Arguments)
    & $gitPath @Arguments
}

Write-Host "🚀 SentiPort GitHub Setup" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan

# Step 1: Initialize repository
Write-Host "`n1️⃣  Initializing Git repository..." -ForegroundColor Yellow
Run-Git init

# Step 2: Configure Git
Write-Host "`n2️⃣  Configuring Git user..." -ForegroundColor Yellow
Run-Git config user.name $GitName
Run-Git config user.email $GitEmail

# Step 3: Check status
Write-Host "`n3️⃣  Checking repository status..." -ForegroundColor Yellow
Run-Git status

# Step 4: Add all files
Write-Host "`n4️⃣  Staging all files..." -ForegroundColor Yellow
Run-Git add .

# Step 5: Create initial commit
Write-Host "`n5️⃣  Creating initial commit..." -ForegroundColor Yellow
Run-Git commit -m "Initial commit: Complete SentiPort project setup with components, hooks, and utilities"

# Step 6: Show commit log
Write-Host "`n6️⃣  Commit history:" -ForegroundColor Yellow
Run-Git log --oneline

Write-Host "`n✅ Git initialized successfully!" -ForegroundColor Green
Write-Host "`n📝 Next steps:" -ForegroundColor Cyan
Write-Host "1. Create a repository on GitHub: https://github.com/new" -ForegroundColor White
Write-Host "2. Name it: SentiPort" -ForegroundColor White
Write-Host "3. Do NOT initialize with README" -ForegroundColor White
Write-Host "4. Copy the repository HTTPS URL" -ForegroundColor White
Write-Host "5. Run this command (replace URL):" -ForegroundColor White
Write-Host "   & 'C:\Program Files\Git\bin\git.exe' remote add origin https://github.com/YOUR_USERNAME/SentiPort.git" -ForegroundColor Cyan
Write-Host "   & 'C:\Program Files\Git\bin\git.exe' branch -M main" -ForegroundColor Cyan
Write-Host "   & 'C:\Program Files\Git\bin\git.exe' push -u origin main" -ForegroundColor Cyan
